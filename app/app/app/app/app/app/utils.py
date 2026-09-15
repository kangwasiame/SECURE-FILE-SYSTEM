def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0 Bytes"
    
    units = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(units) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {units[i]}"

def get_file_icon(filename):
    """Get icon class based on file extension"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    icons = {
        'pdf': 'fa-file-pdf',
        'doc': 'fa-file-word',
        'docx': 'fa-file-word',
        'xls': 'fa-file-excel',
        'xlsx': 'fa-file-excel',
        'ppt': 'fa-file-powerpoint',
        'pptx': 'fa-file-powerpoint',
        'txt': 'fa-file-alt',
        'png': 'fa-file-image',
        'jpg': 'fa-file-image',
        'jpeg': 'fa-file-image',
        'gif': 'fa-file-image',
        'zip': 'fa-file-archive',
    }
    
    return icons.get(ext, 'fa-file')