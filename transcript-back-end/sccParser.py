import openai
from bs4 import BeautifulSoup
import re
import json
import datetime

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
        f.write('<html>\n<body>\n')
        for lang in captions.get_languages():
            captions_lang = captions.get_captions(lang)
            for caption in captions_lang:
                f.write(f'<p>{caption.get_text()}</p>\n')
        f.write('</body>\n</html>')


def reformat_html(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()

    # Split the content into lines
    lines = content.split('\n')

    # Join lines for each speaker's speech
    formatted_lines = []
    for line in lines:
        if line.startswith('<p>- '):
            if ':' in line:

                # Formatting speaker names (bolding them)
                formatted_line = line[5:]
                split_index = formatted_line.find(':') + 1
                first_part = formatted_line[:split_index]
                second_part = formatted_line[split_index + 1:].strip()
                first_part = f'<b>{first_part}</b>'
                combined_string = first_part + " " + second_part
                formatted_lines.append(combined_string)
            else:
                formatted_lines.append(line[5:])
        elif line.startswith('<p>['):

            # Formatting non-verbal sounds
            sound_text = line[3:-4]
            formatted_lines.append(f'<p><i>{sound_text}</i></p>')

        elif line.startswith('<p>'):
            previous = formatted_lines[-1][:-4]
            if previous[-1] == '.':
                formatted_lines.append(line)
            else:
                formatted_lines[-1] = previous + ' ' + line[3:]
        else:
            formatted_lines.append(line)

    # Write the formatted content to the output file
    with open(output_file, 'w') as f:
        f.write('\n'.join(formatted_lines))

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
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
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

# generate the unformatted html file
input_file = "../CaptionSamples/Sample1/2BAW0101HDST.scc"
output_file = "../CaptionSamples/Sample1/sample1_scc.html"
scc_to_html(input_file, output_file)

# format html file
input_file = "../CaptionSamples/Sample1/sample1_scc.html"
output_file = "../CaptionSamples/Sample1/sample1_scc_formatted.html"
reformat_html(input_file, output_file)

# Remove irrelevant sound from the file
input_file = "../CaptionSamples/Sample1/sample1_scc.html"
output_file = "../CaptionSamples/Sample1/sample1_scc_analyzed.html"
analyze_relevance(input_file, output_file)

# fragments json file
input_file = "../CaptionSamples/Sample1/sample1_scc.html"
output_file = "../CaptionSamples/Sample1/sample1_fragments.json"
scc_to_json_F(input_file, output_file)
