from datetime import datetime, timezone

from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    files = db.relationship('File', backref='owner', lazy=True, cascade='all, delete-orphan')


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    file_type = db.Column(db.String(100))
    file_hash = db.Column(db.String(64), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pin = db.relationship('FilePin', backref='file', uselist=False,
                          cascade='all, delete-orphan')
    share = db.relationship('FileShare', backref='file', uselist=False,
                            cascade='all, delete-orphan')


class FilePin(db.Model):
    __tablename__ = 'file_pins'
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), unique=True, nullable=False)
    pin_hash = db.Column(db.String(255), nullable=False)


class FileShare(db.Model):
    __tablename__ = 'file_shares'
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), unique=True, nullable=False)
    code = db.Column(db.String(8), unique=True, nullable=False, index=True)


class PinRecovery(db.Model):
    __tablename__ = 'pin_recoveries'
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    code_hash = db.Column(db.String(255), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)
    file = db.relationship('File', backref=db.backref('pin_recoveries', cascade='all, delete-orphan'))
