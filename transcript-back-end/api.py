from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from sccParser import scc_to_html, reformat_html

app = Flask(__name__)
CORS(app)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"msg": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file:
        input_file = 'input.scc'
        output_file = 'output.html'
        reformatted_file = 'reformat.html'

        file.save(input_file)

        scc_to_html(input_file, output_file)
        reformat_html(output_file, reformatted_file)
        
        return send_file(reformatted_file, as_attachment=True)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)  # Debug mode allows you to see changes without restarting the server