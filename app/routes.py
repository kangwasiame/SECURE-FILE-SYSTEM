import hashlib
import os
import secrets
import smtplib
import uuid
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

from flask import Blueprint, abort, current_app, flash, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import File, FilePin, PinRecovery
from app.utils import format_file_size, get_file_icon

main_bp = Blueprint('main', __name__)


def allowed_file(filename):
    return bool(filename and filename.strip())


@main_bp.get('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html', hero_video_url=current_app.config['HERO_VIDEO_URL'])


@main_bp.get('/secure-file-system')
@main_bp.get('/secure-file-system/')
def named_entry():
    return redirect(url_for('main.index'))


@main_bp.get('/dashboard')
@login_required
def dashboard():
    files = File.query.filter_by(owner_id=current_user.id).order_by(File.uploaded_at.desc()).all()
    return render_template('dashboard.html', files=files, format_file_size=format_file_size, get_file_icon=get_file_icon)


@main_bp.get('/tutorial')
def tutorial():
    return render_template('tutorial.html')


@main_bp.post('/upload')
@login_required
def upload_file():
    uploaded = request.files.get('file')
    pin = request.form.get('pin', '')
    if not uploaded or not uploaded.filename:
        flash('Choose a file before uploading.', 'error')
        return redirect(url_for('main.dashboard'))
    if not pin.isdigit() or len(pin) != 4:
        flash('Choose a 4-digit PIN to protect this file.', 'error')
        return redirect(url_for('main.dashboard'))
    if not allowed_file(uploaded.filename):
        flash('That file type is not supported.', 'error')
        return redirect(url_for('main.dashboard'))
    original_name = secure_filename(uploaded.filename) or 'uploaded-file'
    stored_name = f'{uuid.uuid4().hex}_{original_name}'
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], stored_name)
    try:
        data = uploaded.read()
        with open(path, 'wb') as output:
            output.write(data)
        stored_file = File(filename=stored_name, original_filename=original_name,
                   file_size=len(data), file_type=uploaded.content_type,
                   file_hash=hashlib.sha256(data).hexdigest(), owner_id=current_user.id)
        stored_file.pin = FilePin(pin_hash=generate_password_hash(pin))
        db.session.add(stored_file)
        db.session.commit()
        flash(f'{original_name} uploaded successfully.', 'success')
    except OSError:
        db.session.rollback()
        if os.path.exists(path):
            os.remove(path)
        flash('The file could not be stored.', 'error')
    return redirect(url_for('main.dashboard'))


@main_bp.route('/download/<int:file_id>', methods=['GET', 'POST'])
@login_required
def download_file(file_id):
    file = db.get_or_404(File, file_id)
    if file.owner_id != current_user.id:
        abort(403)
    if not file.pin:
        abort(403)
    if request.method == 'GET':
        return render_template('verify_download.html', file=file)
    pin = request.form.get('pin', '')
    if not pin.isdigit() or len(pin) != 4 or not check_password_hash(file.pin.pin_hash, pin):
        flash('Incorrect 4-digit PIN.', 'error')
        return render_template('verify_download.html', file=file), 401
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], file.filename,
                               as_attachment=True, download_name=file.original_filename)


def send_recovery_code(user, code, filename):
    config = current_app.config
    if not all((config['SMTP_HOST'], config['SMTP_USERNAME'], config['SMTP_PASSWORD'], config['SMTP_FROM'])):
        return False
    message = EmailMessage()
    message['Subject'] = f'Vault PIN recovery code for {filename}'
    message['From'] = config['SMTP_FROM']
    message['To'] = user.email
    message.set_content(f'Your Vault PIN recovery code is {code}. It expires in 10 minutes.')
    with smtplib.SMTP(config['SMTP_HOST'], config['SMTP_PORT'], timeout=15) as smtp:
        smtp.starttls()
        smtp.login(config['SMTP_USERNAME'], config['SMTP_PASSWORD'])
        smtp.send_message(message)
    return True


@main_bp.route('/recover-pin/<int:file_id>', methods=['GET', 'POST'])
@login_required
def recover_pin(file_id):
    file = db.get_or_404(File, file_id)
    if file.owner_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        code = f'{secrets.randbelow(1000000):06d}'
        recovery = PinRecovery(file_id=file.id, code_hash=generate_password_hash(code),
                               expires_at=datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=10))
        db.session.add(recovery)
        db.session.commit()
        try:
            sent = send_recovery_code(current_user, code, file.original_filename)
        except (OSError, smtplib.SMTPException):
            sent = False
        if not sent:
            db.session.delete(recovery)
            db.session.commit()
            flash('Email recovery is not configured. Set SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD, and SMTP_FROM.', 'error')
            return redirect(url_for('main.download_file', file_id=file.id))
        flash(f'A recovery code was sent to {current_user.email}.', 'success')
        return redirect(url_for('main.verify_recovery', recovery_id=recovery.id))
    return render_template('recover_pin.html', file=file, email=current_user.email)


@main_bp.route('/recover-pin/verify/<int:recovery_id>', methods=['GET', 'POST'])
@login_required
def verify_recovery(recovery_id):
    recovery = db.get_or_404(PinRecovery, recovery_id)
    file = recovery.file
    if file.owner_id != current_user.id:
        abort(403)
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    if recovery.used or recovery.expires_at <= now:
        abort(410, description='This recovery code has expired.')
    if request.method == 'POST':
        code = request.form.get('code', '')
        new_pin = request.form.get('new_pin', '')
        if not check_password_hash(recovery.code_hash, code):
            flash('The recovery code is incorrect.', 'error')
        elif not new_pin.isdigit() or len(new_pin) != 4:
            flash('Choose a new 4-digit PIN.', 'error')
        else:
            file.pin.pin_hash = generate_password_hash(new_pin)
            recovery.used = True
            db.session.commit()
            flash('PIN changed. Enter the new PIN to download your file.', 'success')
            return redirect(url_for('main.download_file', file_id=file.id))
    return render_template('verify_recovery.html', file=file)


@main_bp.post('/delete/<int:file_id>')
@login_required
def delete_file(file_id):
    file = db.get_or_404(File, file_id)
    if file.owner_id != current_user.id:
        abort(403)
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    if os.path.exists(path):
        os.remove(path)
    db.session.delete(file)
    db.session.commit()
    flash(f'{file.original_filename} deleted.', 'success')
    return redirect(url_for('main.dashboard'))


@main_bp.get('/api/files')
@login_required
def get_files_api():
    files = File.query.filter_by(owner_id=current_user.id).all()
    return jsonify([{'id': file.id, 'name': file.original_filename, 'size': file.file_size,
                     'type': file.file_type, 'uploaded': file.uploaded_at.isoformat()} for file in files])
