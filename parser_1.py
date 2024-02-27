from flask import Flask, request, render_template
import re

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.srt'):
        srt_content = file.read().decode('utf-8')
        html_transcript = parse_srt(srt_content)
        return html_transcript
    return 'Invalid file type'

if __name__ == '__main__':
    app.run(debug=True)
