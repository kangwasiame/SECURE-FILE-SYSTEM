def format_file_size(size_bytes):
    if size_bytes == 0:
        return '0 Bytes'
    units = ('Bytes', 'KB', 'MB', 'GB', 'TB')
    size = float(size_bytes)
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    return f'{size:.1f} {units[unit_index]}'


def get_file_icon(filename):
    extension = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return {
        'pdf': 'file-pdf', 'doc': 'file-text', 'docx': 'file-text',
        'xls': 'table-2', 'xlsx': 'table-2', 'ppt': 'presentation',
        'pptx': 'presentation', 'png': 'image', 'jpg': 'image',
        'jpeg': 'image', 'gif': 'image', 'txt': 'file-text',
    }.get(extension, 'file')
