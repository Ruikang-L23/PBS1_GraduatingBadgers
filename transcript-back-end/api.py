from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from transcriptParser import scc_to_html, srt_to_html, reformat_html
from utils import is_allowed_file, get_extension
from aiUtils import toggle_mode, analyze_relevance, correct_grammar, remove_filler_words, organize_by_subject_matter

app = Flask(__name__)
CORS(app)

# TODO: Add more error checking here to make the other parameters exist. If they don't we should send a 400 with an error message, currently it will just send a 500.
@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"msg": "No file attached in request."}), 400
    
    # Check that caption is in either a SCC or SRT file format.
    file = request.files['file']
    file_name = file.filename
    if not is_allowed_file(file_name):
        return jsonify({"msg": "Included file was not in an accepted format."}), 415

    # Convert italics flag to Python boolean.
    italics_state = request.form['italicizeCues']
    if 'true' in italics_state:
        italics_state = True
    else:    
        italics_state = False
        
    # Convert timestamp flag to Python boolean.
    timestamp_state = request.form['enableTimestamps']
    if 'true' in timestamp_state:
        timestamp_state = True
    else:
        timestamp_state = False

    # Initialize all files and file names for transcription process.
    input_file = 'input.' + get_extension(file_name)
    output_file = 'output.html'
    reformatted_file = 'reformat.html'
    file.save(input_file)

    # Parse caption file to create transcript.
    if get_extension(file_name) == 'srt':
        srt_to_html(input_file, output_file, timestamp_state)
    else:
        scc_to_html(input_file, output_file, timestamp_state)
    reformat_html(output_file, reformatted_file, italics_state)
        
    return send_file(reformatted_file, as_attachment=True), 200

# TODO: Add more error checking here to make the other parameters exist. If they don't we should send a 400 with an error message, currently it will just send a 500.
@app.route('/api/upload-ai', methods=['POST'])
def upload_file_ai():
    # Check that caption file is contained in request form.
    if 'file' not in request.files:
        return jsonify({"msg": "No file attached in request."}), 400
    
    # Check that caption is in either a SCC or SRT file format.
    file = request.files['file']
    file_name = file.filename
    if not is_allowed_file(file_name):
        return jsonify({"msg": "Included file was not in an accepted format."}), 415
    
    # Convert italics flag to Python boolean.
    italics_state = request.form['italicizeCues']
    if 'true' in italics_state:
        italics_state = True
    else:    
        italics_state = False
        
    # Convert timestamp flag to Python boolean.
    timestamp_state = request.form['enableTimestamps']
    if 'true' in timestamp_state:
        timestamp_state = True
    else:
        timestamp_state = False

    # Store transcription mode from request form in a variable.
    transcription_mode = request.form['transcriptionMode']

    # Initialize all files and file names for transcription process.
    input_file = 'input.' + get_extension(file_name)
    output_file = 'output.html'
    reformatted_file = 'reformat.html'
    ai_reformatted_file = 'aiReformat.html'
    file.save(input_file)

    # Parse caption file to create transcript.
    if get_extension(file_name) == 'srt':
        srt_to_html(input_file, output_file, timestamp_state)
    else:
        scc_to_html(input_file, output_file, timestamp_state)
    reformat_html(output_file, reformatted_file, italics_state)
    if transcription_mode == 'verbatim':
        organize_by_subject_matter(reformatted_file, ai_reformatted_file)
    else:
        # We need to merge our organize paragraphs by subject matter and correct grammar functions into one AI prompt to minimize runtime.
        organize_by_subject_matter(reformatted_file, ai_reformatted_file)

    return send_file(ai_reformatted_file, as_attachment=True), 200

if __name__ == '__main__':
    app.run(debug=True)