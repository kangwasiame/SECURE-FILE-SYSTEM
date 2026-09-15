import os
from datetime import timedelta

class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.environ.get('DATA_DIR', BASE_DIR)
    APP_NAME = os.environ.get('APP_NAME', 'Secure File System')
    PUBLIC_BASE_URL = os.environ.get('PUBLIC_BASE_URL', 'http://127.0.0.1:5000/secure-file-system')
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', '5000'))
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-only-change-this-secret')
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(DATA_DIR, 'secure_storage.db'),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(DATA_DIR, 'uploads'))
    HERO_VIDEO_URL = os.environ.get(
        'HERO_VIDEO_URL',
        'https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4',
    )
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
    ALLOWED_EXTENSIONS = None
    SMTP_HOST = os.environ.get('SMTP_HOST')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
    SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    SMTP_FROM = os.environ.get('SMTP_FROM', SMTP_USERNAME)