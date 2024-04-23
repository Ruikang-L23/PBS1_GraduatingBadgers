from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
from transcriptParser import scc_to_html, srt_to_html, reformat_html
from utils import is_allowed_file, get_extension
from aiUtils import toggle_mode, analyze_relevance, correct_grammar, remove_filler_words, organize_by_subject_matter

app = Flask(__name__)
CORS(app)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"msg": "An error occurred: No caption file included in request."}), 400
    
    # Check that caption is in either a SCC or SRT file format.
    file = request.files['file']
    file_name = file.filename
    if not is_allowed_file(file_name):
        return jsonify({"msg": f"An error occurred: '{get_extension(file_name).upper()}' is not an accepted caption file format."}), 415

    # Check for necessary flags and convert them to Python booleans.
    try:
        italics_state = request.form['italicizeCues']
        italics_state = True if 'true' in italics_state.lower() else False
    except KeyError as e:
        return jsonify({"msg": "An error occurred: italicizeCues was not included in request."}), 400
    try:
        timestamp_state = request.form['enableTimestamps']
        timestamp_state = True if 'true' in timestamp_state.lower() else False
    except KeyError as e:
        return jsonify({"msg": "An error occurred: enableTimestamps was not included in request."}), 400

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

    response = make_response(send_file(reformatted_file, as_attachment=True))
    response.headers['Access-Control-Allow-Origin'] = '*'
        
    return response, 200

@app.route('/api/upload-ai', methods=['POST'])
def upload_file_ai():
    # Check that caption file is contained in request form.
    if 'file' not in request.files:
        return jsonify({"msg": "An error occurred: No caption file included in request."}), 400
    
    # Check that caption is in either a SCC or SRT file format.
    file = request.files['file']
    file_name = file.filename
    if not is_allowed_file(file_name):
        return jsonify({"msg": f"An error occurred: '{get_extension(file_name).upper()}' is not an accepted caption file format."}), 415
    
    # Check for necessary flags and convert them to Python booleans.
    try:
        italics_state = request.form['italicizeCues']
        italics_state = True if 'true' in italics_state.lower() else False
    except KeyError as e:
        return jsonify({"msg": "An error occurred: italicizeCues was not included in request."}), 400
    try:
        timestamp_state = request.form['enableTimestamps']
        timestamp_state = True if 'true' in timestamp_state.lower() else False
    except KeyError as e:
        return jsonify({"msg": "An error occurred: enableTimestamps was not included in request."}), 400

    # Store transcription mode from request form in a variable.
    try:
        transcription_mode = request.form['transcriptionMode']
        if transcription_mode != 'verbatim' and transcription_mode != 'non-verbatim':
            return jsonify({"msg": "An error occurred: transcriptionMode must have value of either 'verbatim' or 'non-verbatim'."}), 400    
    except KeyError as e:
        return jsonify({"msg": "An error occurred: transcriptionMode was not included in request."}), 400

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
        # Function to remove filler words here.
        # Organize by subject matter and correct grammar prompt here.
        organize_by_subject_matter(reformatted_file, ai_reformatted_file)

    response = make_response(send_file(ai_reformatted_file, as_attachment=True))
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response, 200

if __name__ == '__main__':
    app.run(debug=True)