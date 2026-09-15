from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import File
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime

main_bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    files = File.query.filter_by(owner_id=current_user.id).order_by(File.uploaded_at.desc()).all()
    return render_template('dashboard.html', files=files)

@main_bp.route('/tutorial')
def tutorial():
    """Display the tutorial page"""
    return render_template('tutorial.html')

@main_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('main.dashboard'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('main.dashboard'))
    
    if not allowed_file(file.filename):
        flash('File type not allowed. Allowed: txt, pdf, png, jpg, jpeg, gif, doc, docx, xls, xlsx, ppt, pptx', 'error')
        return redirect(url_for('main.dashboard'))
    
    try:
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
        file_path = os.path.join(upload_folder, unique_filename)
        
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        db_file = File(
            filename=unique_filename,
            original_filename=filename,
            file_size=file_size,
            file_type=file.content_type,
            encrypted_path=file_path,
            owner_id=current_user.id
        )
        
        db.session.add(db_file)
        db.session.commit()
        
        flash(f'✅ File "{filename}" uploaded successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error uploading file: {str(e)}', 'error')
    
    return redirect(url_for('main.dashboard'))

@main_bp.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    file = File.query.get_or_404(file_id)
    
    if file.owner_id != current_user.id:
        flash('❌ You can only delete your own files', 'error')
        return redirect(url_for('main.dashboard'))
    
    try:
        if os.path.exists(file.encrypted_path):
            os.remove(file.encrypted_path)
        
        db.session.delete(file)
        db.session.commit()
        
        flash(f'✅ File "{file.original_filename}" deleted successfully', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error deleting file: {str(e)}', 'error')
    
    return redirect(url_for('main.dashboard'))

@main_bp.route('/api/files')
@login_required
def get_files_api():
    files = File.query.filter_by(owner_id=current_user.id).all()
    file_list = []
    for file in files:
        file_list.append({
            'id': file.id,
            'name': file.original_filename,
            'size': file.file_size,
            'type': file.file_type,
            'uploaded': file.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(file_list)