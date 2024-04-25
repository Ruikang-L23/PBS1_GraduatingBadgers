import openai
import re
import string
import os
from bs4 import BeautifulSoup
from organizeBySubjectMatter import organize_paragraphs_by_subject_matter

# Remove the irrelevant sound with chatGPT plugin
def analyze_relevance(input_file, output_file):
    with open(input_file, 'r') as f:
        formatted_content = f.read()

    soup = BeautifulSoup(formatted_content, "html.parser")

    # Extract non-verbal sounds
    non_verbal_sounds = [tag.get_text() for tag in soup.find_all("i")]

    # Set your API key as an environment variable on your computer with the name OpenAI.
    openai.api_key = os.environ["OpenAI"]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Determine the context: " + soup.get_text()},
        ]
    )
    context = response.choices[0].message['content']

    # Check if the extracted sound is relevant to the context
    irrelevant_sounds = [sound for sound in non_verbal_sounds if not any(keyword in context.lower() for keyword in sound.lower().split(', '))]

    # Remove irrelevant non-verbal sounds from the HTML content
    for sound in irrelevant_sounds:
        for tag in soup.find_all("i"):
            if tag.get_text() == sound:
                tag.decompose()

    with open(output_file, 'w') as f:
        f.write(str(soup))

def analyze_relevance_reg(input_file, output_file):

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
def correct_grammar(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()

    # Splitting the content into smaller chunks to ensure they are under the token limit
    max_length = 16000  # A bit under the limit to account for additional tokens added by the prompt
    content_chunks = [content[i:i+max_length] for i in range(0, len(content), max_length)]
    openai.api_key = os.environ["OpenAI"]
    corrected_chunks = []

    for chunk in content_chunks:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Correct the grammar: " + chunk},
            ]
        )
        corrected_chunk = response.choices[0].message['content']
        corrected_chunks.append(corrected_chunk)

    corrected_content = ''.join(corrected_chunks)

    with open(output_file, 'w') as f:
        f.write(corrected_content)

FILLER_WORDS = ["uh", "um", "er", "ah", "hmm", "you know", "basically",
                "actually", "kind of", "sort of", "i mean", "right", "okay"]

def remove_filler_words(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    for p in soup.find_all('p'):
        # Split text by words and non-words, keeping the delimiters (punctuation, spaces, etc.)
        text_parts = re.split(r'(\b\w+\b|\W+)', p.get_text())
        
        # Reconstruct the text, skipping only the filler words, not the punctuation or spaces
        new_text = ''.join(part for part in text_parts if part.lower().strip() not in FILLER_WORDS)
        
        p.string = new_text.strip()

    return str(soup)

# In the toggle_mode function, replace the call to remove_filler_words with this new implementation.
def toggle_mode(input_file, mode):
    if mode not in ['verbatim', 'non-verbatim']:
        raise ValueError("Mode must be 'verbatim' or 'non-verbatim'")

    if mode == 'non-verbatim':
        #corrected_file = input_file.replace('.html', '_corrected.html')
        corrected_file = input_file
        #Run the grammar correction function to generate the corrected content
        #correct_grammar_parallel(input_file, corrected_file)

        # Open the corrected file for reading
        with open(corrected_file, 'r') as f:
            corrected_content = f.read()

        # Perform filtering and create the non-verbatim file
        filtered_content = remove_filler_words(corrected_content)
        #filtered_file = input_file.replace('.html', '_nonverbatim.html')
        filtered_file = input_file.replace('.html', '.html')
        with open(filtered_file, 'w') as f:
            f.write(filtered_content)

def organize_by_subject_matter(input_file, output_file, transcription_mode):
    organize_paragraphs_by_subject_matter(input_file, output_file, transcription_mode)

# Remove irrelevant sound from the file
# input_file = "../CaptionSamples/Sample1/sample1_scc.html"
# output_file = "../CaptionSamples/Sample1/sample1_scc_analyzed.html"
# analyze_relevance(input_file, output_file)


# Non-Verbatim mode
# input_file = "../CaptionSamples/Sample1/sample1_scc.html"
# mode = "non-verbatim"
# input_file = "../CaptionSamples/Sample1/mini.html"
# toggle_mode(input_file, mode)

