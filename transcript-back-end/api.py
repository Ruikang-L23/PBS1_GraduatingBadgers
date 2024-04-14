from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from transcriptParser import scc_to_html, srt_to_html, reformat_html
from utils import is_allowed_file, get_extension
from aiUtils import toggle_mode, analyze_relevance, correct_grammar, remove_filler_words
from organizeBySubjectMatter import organize_paragraphs_by_subject_matter

app = Flask(__name__)
CORS(app)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"msg": "No file attached in request."}), 400
    
    file = request.files['file']
    file_name = file.filename

    # Check flag that determines whether to italicize non-verbal sounds.
    italics_state = request.form['italics']
    if 'true' in italics_state:
        italics_state = True
    else:    
        italics_state = False

    # Check flag that determines whether to utilize AI tools in transcript generation.
    ai_state = request.form['ai']
    if 'true' in ai_state:
        ai_state = True
    else:
        ai_state = False

    transcription_mode = request.form['transcriptionMode']

    if transcription_mode == 'non-verbatim' and ai_state == False:
        return jsonify({"msg": "Non-Verbatim transcription is not possible with AI usage disabled."})

    if not is_allowed_file(file_name):
        return jsonify({"msg": "Included file was not in an accepted format."}), 415
    
    if file and get_extension(file_name) == 'srt':
        input_file = 'input.srt'
        output_file = 'output.html'
        reformatted_file = 'reformat.html'

        file.save(input_file)

        srt_to_html(input_file, output_file)
        reformat_html(output_file, reformatted_file, italics_state)
        if ai_state:
            if transcription_mode == 'non-verbatim':
                # TODO ask Oliver if the input file is already formatted and has italics <i> for the sounds 
                analyze_relevance(reformatted_file, reformatted_file)
                toggle_mode(reformatted_file, "non-verbatim")
                organize_paragraphs_by_subject_matter(reformatted_file, reformatted_file)
                # Run all AI formatting on reformatted_file if this flag is true.
                # This means removing filler words, correcting grammar, and removing unrelated non-verbal cues.
                # As well as, grouping paragraphs together by their context within the transcript.
                print("Not yet implemented.\n")
            else:
                organize_paragraphs_by_subject_matter(reformatted_file, reformatted_file)
                analyze_relevance(reformatted_file, reformatted_file)
                # Run only AI formatting that will not change the content of the transcript.
                # This only includes grouping paragraphs together by their context.
                # Possibly includes removing unrelated non-verbal cues.
                print("Not yet implemented\n")
                

        return send_file(reformatted_file, as_attachment=True), 200

    if file and get_extension(file_name) == 'scc':
        input_file = 'input.scc'
        output_file = 'output.html'
        reformatted_file = 'reformat.html'

        file.save(input_file)

        scc_to_html(input_file, output_file)
        reformat_html(output_file, reformatted_file, italics_state)
        if ai_state:
            if transcription_mode == 'non-verbatim':
                analyze_relevance(reformatted_file, reformatted_file)
                toggle_mode(reformatted_file, "non-verbatim")
                organize_paragraphs_by_subject_matter(reformatted_file, reformatted_file)
                # Run all AI formatting on reformatted_file if this flag is true.
                # This means removing filler words, correcting grammar, and removing unrelated non-verbal cues.
                # As well as, grouping paragraphs together by their context within the transcript.
                print("Not yet implemented.\n")
            else:
                organize_paragraphs_by_subject_matter(reformatted_file, reformatted_file)
                analyze_relevance(reformatted_file, reformatted_file)
                # Run only AI formatting that will not change the content of the transcript.
                # This only includes grouping paragraphs together by their context.
                # Possibly includes removing unrelated non-verbal cues.
                print("Not yet implemented\n")
        
        return send_file(reformatted_file, as_attachment=True), 200

# This should be added in another ticket (PBS-38).
# It will make working with the transcript on the frontend much easier and allow us to add more features.
@app.route('/api/upload-json', methods=['POST'])
def upload_file_json():
    return jsonify({"msg": "Caption file to JSON conversion is not yet implemented."}), 501

if __name__ == '__main__':
    app.run(debug=True)
