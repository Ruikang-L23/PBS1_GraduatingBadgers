from bs4 import BeautifulSoup
import json
from utils import float_to_time_format
from aiUtils import analyze_relevance, correct_grammar, remove_filler_words, toggle_mode
from pycaption import SCCReader
from pycaption import SRTReader

def scc_to_html(input_file, output_file, time_stamp = False):
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
                if time_stamp == True:
                    f.write(f'<p data-timestamp-start={start} data-timestamp-end={end}>{caption.get_text()}</p>\n<br>\n')
                else:
                    f.write(f'<p>{caption.get_text()}</p>\n<br>\n')
        if time_stamp == True:
            f.write('<script src="script.js"></script>\n</body>\n</html>')
        else:
            f.write('</body>\n</html>')

def srt_to_html(input_file, output_file, time_stamp = False):
    with open(input_file, 'r', encoding='ISO-8859-1') as f:
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
                if time_stamp == True:
                    f.write(f'<p data-timestamp-start={start} data-timestamp-end={end}>{caption.get_text()}</p>\n<br>\n')
                else:
                    f.write(f'<p>{caption.get_text()}</p>\n<br>\n')
        if time_stamp == True:
            f.write('<script src="script.js"></script>\n</body>\n</html>')
        else:
            f.write('</body>\n</html>')

def reformat_html(input_file, output_file, italics_state):
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
                # Print out the text, this could be changed to Speaker: or Unknown: is desired.
                formatted_text = f'- {text[2:]}'
            
        # Case 2: If the text starts with "["
        elif text.startswith("["):
            # Italicize the text
            formatted_text = '<i>' + text + '</i>' if italics_state else text
            formatted_text = formatted_text.replace("]\n[", "]</i><br \><i>[")

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

def scc_to_json(input_file, output_file):
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

def html_to_txt(input_html, output_txt):
    with open(input_html, 'r', encoding='utf-8') as f:
        html_content = f.read()

    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(html_content)