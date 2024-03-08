from flask import Flask, request, jsonify
import openai
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure your OpenAI API key here
openai.api_key = os.getenv('OPENAI_API_KEY', 'your_openai_api_key_here')

# Ensure you have this folder for uploads, or configure it as per your requirements
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'srtFile' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['srtFile']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        story = convert_srt_to_story(filepath)
        return jsonify({'story': story})

def convert_srt_to_story(filepath):
    srt_text = open(filepath, 'r', encoding='utf-8').read()
    dialogues = process_srt_text(srt_text)
    story = generate_story_with_openai(dialogues)
    return story

def process_srt_text(srt_text):
    # Simple SRT parser (For demonstration, may need improvements)
    lines = srt_text.split('\n')
    dialogues = []
    for line in lines:
        if not line.isdigit() and '-->' not in line and line != '':
            dialogues.append(line)
    clean_text = ' '.join(dialogues)
    return clean_text

def generate_story_with_openai(dialogues):
    try:
        # Call OpenAI API to generate story from dialogues
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the most suitable engine you have access to
            prompt=f"Convert the following dialogues into a readable story:\n\n{dialogues}",
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
