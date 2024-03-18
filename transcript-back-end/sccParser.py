from bs4 import BeautifulSoup
import re
import json
import datetime
import string

try:
    from pycaption import SCCReader
except ImportError:
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "pycaption"])
    from pycaption import SCCReader

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
        paragraph.string.replace_with(BeautifulSoup(formatted_text, 'html.parser'))

        # Update the previous paragraph
        prev_paragraph = paragraph

    # Write the updated HTML content to a new file
    with open(output_file, 'w') as f:
        f.write(str(soup))

def float_to_time_format(float_mmm):
    # Convert float microseconds to a timedelta object
    timedelta = datetime.timedelta(microseconds=float_mmm)
    # Convert timedelta to a string in the desired format
    time_format = str(timedelta)
    # Extract hours, minutes, seconds, and milliseconds
    parts = time_format.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2].split('.')[0])
    milliseconds = int(parts[2].split('.')[1]) if '.' in parts[2] else 0
    # Format the time string with leading zeros
    formatted_time_withMMM = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return formatted_time

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

# generate the unformatted html file
input_file = "../CaptionSamples/Sample1/2BAW0101HDST.scc"
output_file = "../CaptionSamples/Sample1/sample1_scc.html"
scc_to_html(input_file, output_file)

# format html file
input_file = "../CaptionSamples/Sample1/sample1_scc.html"
output_file = "../CaptionSamples/Sample1/sample1_scc_formatted.html"
reformat_html(input_file, output_file)

# fragments json file
input_file = "../CaptionSamples/Sample1/2BAW0101HDST.scc"
output_file = "../CaptionSamples/Sample1/sample1_fragments.json"
scc_to_json_F(input_file, output_file)
