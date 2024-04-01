import openai
import re
import string
import os
from bs4 import BeautifulSoup

# Remove the irrelevant sound with chatGPT plugin
def analyze_relevance(input_file, output_file):

    with open(input_file, 'r') as f:
        formatted_content = f.read()

    # Extract non-verbal sounds
    soup = BeautifulSoup(formatted_content, "html.parser")
    text = soup.get_text()
    non_verbal_sounds = re.findall(r'\[(.*?)\]', text)

    # Set your API key as an environment variable on your computer with the name OpenAI.
    openai.api_key = os.environ["OpenAI"]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Determine the context: " + text},
        ]
    )
    context = response.choices[0].message['content']

    # Check if the extracted sound is relevant to the context
    irrelevant_sounds = [sound for sound in non_verbal_sounds if not any(keyword in context.lower() for keyword in sound.lower().split(', '))]
    #print("Relevant Non-verbal Sounds:", irrelevant_sounds)
    for sound in irrelevant_sounds:
        pattern = re.compile(r'<p><i>\[' + re.escape(sound) + r'\]</i></p>')
        formatted_content = pattern.sub('', formatted_content)

    with open(output_file, 'w') as f:
        f.write(formatted_content)

# Non-Verbatim transcript conversion
def correct_grammar(text):
    # Use the ChatGPT plugin to correct grammatical errors in the text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Correct the grammar: " + text},
        ]
    )
    corrected_text = response.choices[0].message['content']
    return corrected_text

FILLER_WORDS = ['um', 'uh', 'ah', 'like']
def remove_filler_words(text):
    words = text.split()
    # Create a translation table for removing punctuation
    translator = str.maketrans('', '', string.punctuation)
    filtered_words = []
    for word in words:
        # Remove punctuation from the word for comparison
        stripped_word = word.translate(translator).lower()
        if stripped_word not in FILLER_WORDS:
            filtered_words.append(word)
    return ' '.join(filtered_words)

def toggle_mode(transcript, mode):
    if mode not in ['verbatim', 'non-verbatim']:
        raise ValueError("Mode must be 'verbatim' or 'non-verbatim'")

    if mode == 'verbatim':
        return correct_grammar(transcript)

    return remove_filler_words(transcript)