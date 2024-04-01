import datetime

allowed_extensions = {'srt', 'scc'}

def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()

def float_to_time_format(float_mmm):
    # Convert float microseconds to a timedelta object
    timedelta = datetime.timedelta(microseconds=float_mmm)
    # Convert timedelta to a string in the desired format
    time_format = str(timedelta)
    # Extract hours, minutes, seconds, and milliseconds
    parts = time_format.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2].split('.')[0])
    milliseconds = int(parts[2].split('.')[1]) if '.' in parts[2] else 0
    # Format the time string with leading zeros
    formatted_time_withMMM = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return formatted_time