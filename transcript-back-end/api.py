from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from sccParser import scc_to_html, reformat_html
from utils import is_allowed_file, get_extension

app = Flask(__name__)
CORS(app)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"msg": "No file attached in request."}), 400
    
    file = request.files['file']
    file_name = file.filename

    if not is_allowed_file(file_name):
        return jsonify({"msg": "Included file was not in an accepted format."}), 415
    
    if file and get_extension(file_name) == 'srt':
        return jsonify({"msg": "SRT Parsing is not yet implemented."}), 501

    if file and get_extension(file_name) == 'scc':
        input_file = 'input.scc'
        output_file = 'output.html'
        reformatted_file = 'reformat.html'

        file.save(input_file)

        scc_to_html(input_file, output_file)
        reformat_html(output_file, reformatted_file)
        
        return send_file(reformatted_file, as_attachment=True), 200

if __name__ == '__main__':
    app.run(debug=True)