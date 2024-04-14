from aiUtils import toggle_mode, analyze_relevance, correct_grammar, remove_filler_words
from organizeBySubjectMatter import organize_paragraphs_by_subject_matter

import re
import os
import openai
from bs4 import BeautifulSoup

def analyze_relevanc2e(input_file, output_file):
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

# Non-Verbatim mode
#input_file = "../CaptionSamples/Sample1/sample1_scc.html"
# mode = "non-verbatim"
reformatted_file = "../CaptionSamples/Sample1/mini.html"
#reformatted_file1 = "../CaptionSamples/Sample1/mini_1.html"
# toggle_mode(input_file, mode)
analyze_relevance(reformatted_file, reformatted_file)
toggle_mode(reformatted_file, "non-verbatim")
#remove_filler_words(reformatted_file)
#correct_grammar(reformatted_file, reformatted_file)
organize_paragraphs_by_subject_matter(reformatted_file, reformatted_file)
