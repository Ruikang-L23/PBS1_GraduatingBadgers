allowed_extensions = {'srt', 'scc'}

def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()