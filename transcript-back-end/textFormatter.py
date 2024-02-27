import re
import os

def textFormatter(htmlfile):
    with open(htmlfile, 'r', encoding='utf-8') as file:
        html_content = file.read()

    pattern = re.compile(r'(\w+:.*?)(?=\n\w+:|\Z)', re.DOTALL)

    def replace_func(match):
        return re.sub(r'\n+', ' ', match.group(0)).strip()

    formatted_content = pattern.sub(replace_func, html_content)
    
    #print(formatted_content)
    # Construct the new filename
    new_filename = os.path.splitext(htmlfile)[0] + "converted.html"

    # Write the formatted content to the new file
    with open(new_filename, 'w', encoding='utf-8') as file:
        file.write(formatted_content)

    return new_filename

# Test the function
textFormatter('sampleText.html')

