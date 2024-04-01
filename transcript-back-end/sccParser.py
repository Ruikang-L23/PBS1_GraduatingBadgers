import openai
from bs4 import BeautifulSoup
import re
import json
import string
from utils import float_to_time_format

try:
    from pycaption import SCCReader
except ImportError:
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "pycaption"])
    from pycaption import SCCReader

from pycaption import SRTReader

def scc_to_html(input_file, output_file):
    with open(input_file, 'r') as f:
        scc_content = f.read()

    captions = SCCReader().read(scc_content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('''<html>\n
                    <head>\n
                        <link rel="stylesheet" href="styles.css">
                    </head>\n
                    <body>\n''')
        for lang in captions.get_languages():
            captions_lang = captions.get_captions(lang)
            for caption in captions_lang:
                start = float_to_time_format(caption.start)
                end = float_to_time_format(caption.end)
                f.write(f'<p data-timestamp-start={start} data-timestamp-end={end}>{caption.get_text()}</p>\n<br>\n')
        f.write('<script src="script.js"></script>\n</body>\n</html>')

def srt_to_html(input_file, output_file, encoding='ISO-8859-1'):
    with open(input_file, 'r', encoding=encoding) as f:
        srt_content = f.read()

    captions = SRTReader().read(srt_content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('''<html>\n
                    <head>\n
                        <link rel="stylesheet" href="styles.css">
                    </head>\n
                    <body>\n''')
        for lang in captions.get_languages():
            captions_lang = captions.get_captions(lang)
            for caption in captions_lang:
                start = float_to_time_format(caption.start)
                end = float_to_time_format(caption.end)
                f.write(f'<p data-timestamp-start="{start}" data-timestamp-end="{end}">{caption.get_text()}</p>\n<br>\n')
        f.write('<script src="script.js"></script>\n</body>\n</html>')

def reformat_html(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()

    # # Split the content into lines
    # lines = content.split('\n')
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Get all <p> elements
    pTags = soup.find_all('p')

    # Initialize a variable to keep track of the previous paragraph
    prev_p = None

    # Iterate through each <p> element
    for paragraph in pTags:
        text = paragraph.get_text()

        # Case 1: If the text starts with "- "
        if text.startswith("- "):
            # Check if a colon is present
            if ':' in text:
                # Split the text at the colon to determine the part that needs to be bold
                split_index = text.find(':') + 1
                first_part = text[2:split_index]
                second_part = text[split_index:]
                formatted_text = f'<b>{first_part}</b>{second_part}'
            else:
                # Add "Unknown" to specify missing speaker name
                formatted_text = f'<b>Unknown:</b> {text[2:]}'
            
        # Case 2: If the text starts with "["
        elif text.startswith("["):
            # Italicize the text
            formatted_text = '<i>' + text + '</i>'

        # Case 3: If it is not either case
        else:
            # Determine if the text is the start of a whole sentence
            if prev_paragraph is not None and prev_paragraph.get_text().endswith('.'):
                # Keep it in its own line (no change)
                formatted_text = text
            else:
                # Remove the <br> between this <p> section and the previous <p> section
                if prev_paragraph is not None:
                    br_tag = prev_paragraph.find_next_sibling()
                    if br_tag.name == 'br':
                        br_tag.extract()
                formatted_text = text

        # Update the paragraph's HTML with the formatted text
        #paragraph.string.replace_with(BeautifulSoup(formatted_text, 'html.parser'))
        paragraph.clear()
        paragraph.append(BeautifulSoup(formatted_text, 'html.parser'))

        # Update the previous paragraph
        prev_paragraph = paragraph

    # Write the updated HTML content to a new file
    with open(output_file, 'w') as f:
        f.write(str(soup))

def scc_to_json_F(input_file, output_file):
    with open(input_file, 'r') as f:
        scc_content = f.read()

    captions = SCCReader().read(scc_content)
    
    data = []
    for lang in captions.get_languages():
        captions_lang = captions.get_captions(lang)
        for caption in captions_lang:
            start = caption.start
            end = caption.end
            start = float_to_time_format(start)
            end = float_to_time_format(end)     
            text = caption.get_text()
            data.append({
                'start_time': start,
                'end_time': end,
                'text': text
            })

    # Saving to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=2)

# Remove the irrelevant sound with chatGPT plugin
def analyze_relevance(input_file, output_file):

    with open(input_file, 'r') as f:
        formatted_content = f.read()

    # Extract non-verbal sounds
    soup = BeautifulSoup(formatted_content, "html.parser")
    text = soup.get_text()
    non_verbal_sounds = re.findall(r'\[(.*?)\]', text)

    #OpenAI setting
    openai.api_key = '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'
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

with open('filter_words_test.txt', 'r') as file:
    transcript = file.read()
filtered_transcript = toggle_mode(transcript, 'non-verbatim')
with open('filter_words_tested.txt', 'w') as file:
    file.write(filtered_transcript)

def html_to_txt(input_html, output_txt):
    with open(input_html, 'r', encoding='utf-8') as f:
        html_content = f.read()

    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(html_content)

# generate the unformatted html file
input_file = "../CaptionSamples/Sample1/2BAW0101HDST.scc"
output_file = "../CaptionSamples/Sample1/sample1_scc.html"
scc_to_html(input_file, output_file)
input_file = "../CaptionSamples/Sample1/2BAW0101HDST.srt"
output_file = "../CaptionSamples/Sample1/sample1_srt.html"
srt_to_html(input_file, output_file)

# format html file
input_file = "../CaptionSamples/Sample1/sample1_scc.html"
output_file = "../CaptionSamples/Sample1/sample1_scc_formatted.html"
reformat_html(input_file, output_file)
input_file = "../CaptionSamples/Sample1/sample1_srt.html"
output_file = "../CaptionSamples/Sample1/sample1_srt_formatted.html"
reformat_html(input_file, output_file)

# Remove irrelevant sound from the file
input_file = "../CaptionSamples/Sample1/sample1_scc.html"
output_file = "../CaptionSamples/Sample1/sample1_scc_analyzed.html"
analyze_relevance(input_file, output_file)

# fragments json file
input_file = "../CaptionSamples/Sample1/2BAW0101HDST.scc"
output_file = "../CaptionSamples/Sample1/sample1_fragments.json"
scc_to_json_F(input_file, output_file)

# html to txt
input_file = "../CaptionSamples/Sample1/sample1_scc_formatted.html"
output_file = "../CaptionSamples/Sample1/sample1_scc_formatted.txt"
html_to_txt(input_file, output_file)
input_file = "../CaptionSamples/Sample1/sample1_srt_formatted.html"
output_file = "../CaptionSamples/Sample1/sample1_srt_formatted.txt"
html_to_txt(input_file, output_file)