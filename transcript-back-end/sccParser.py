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


# generate the unformatted html file
input_file = "../CaptionSamples/Sample1/2BAW0101HDST.scc"
output_file = "../CaptionSamples/Sample1/sample1_scc.html"
scc_to_html(input_file, output_file)

# format html file
input_file = "../CaptionSamples/Sample1/sample1_scc.html"
output_file = "../CaptionSamples/Sample1/sample1_scc_formatted.html"
reformat_html(input_file, output_file)
