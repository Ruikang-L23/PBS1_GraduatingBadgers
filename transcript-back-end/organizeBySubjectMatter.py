from bs4 import BeautifulSoup
import openai
from concurrent.futures import ThreadPoolExecutor
import time
import os
import re

start_time = time.time()

def is_new_speaker(tag):
    """Check if the tag introduces a new speaker."""
    return tag.name == 'p' and ((tag.find('b') is not None) or (tag.find('i') is not None))

def remove_breaks_within_speaker_text(html_content):
    """Process the HTML file to remove unnecessary <br> tags and return the cleaned HTML."""

    soup = BeautifulSoup(html_content, 'html.parser')

    for br in soup.find_all('br'):
        next_tag = br.find_next_sibling()
        if not is_new_speaker(next_tag):
            br.decompose()

    with open('clean.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))

    return str(soup)
def split_html_content(html_content, max_length=4000):
    """Splits the HTML content into segments that are within the max_length in characters.
    Adds a space after the last character of text (not including HTML tags)."""
    segments = []
    current_segment = ""

    def add_space_before_last_tag(html_text):
        # This pattern looks for text inside the <p> tag, ensuring not to include any trailing spaces before </p>
        pattern = r'(<p data-timestamp-end="[^"]+" data-timestamp-start="[^"]+">)(.*?)(\S)(\s*?</p>)'
        # This replacement will add a space directly before </p>, preserving any content and initial part of the tag
        replacement = r'\1\2\3 \4'

        # Perform the substitution and return the modified HTML
        modified_html = re.sub(pattern, replacement, html_text, flags=re.DOTALL)
        return modified_html

    for line in html_content.split('\n'):
        prepared_line = line + '\n'
        if len(current_segment) + len(prepared_line) > max_length:
            current_segment = add_space_before_last_tag(current_segment)
            segments.append(current_segment)
            current_segment = prepared_line
        else:
            current_segment += prepared_line

    if current_segment:
        current_segment = add_space_before_last_tag(current_segment)
        segments.append(current_segment)

    return segments

def process_segment_with_chat(segment):
    """Process a single segment of HTML content with GPT using the chat model endpoint."""
    openai.api_key = os.environ["OpenAI"]

    # Prompt to give to ChatGBT API
    prompt_description = """
    In this HTML code, do not remove any <br/>. However, add a <br/> after a ".</p>" if 
    the subject matter before and after the ".</p>" are different. Do not add a <br/> anywhere else.
    Also, do not add <br/> if the next line has a colon (:).
    Also correct any spacing problems (e.g. "ofThe Capital" should change to "of The Capital")

    Don't remove or change ANYTHING else other than this, especially the <html>, <head>, <body> and <link> tags
    Don't alter the start or end, even if it is incomplete code. 
    Don't add any `````` or anything like that.
    Don't say anything else, just output the final fixed HTML code
    """

    # Create a new chat with a single message containing the prompt and the segment
    response = openai.ChatCompletion.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": prompt_description},
            {"role": "user", "content": segment}
        ],
    )

    # Extract and return the text from the chat's response
    if response and 'choices' in response and len(response['choices']) > 0:
        chat_response = response['choices'][0]['message']['content']
        return chat_response
    else:
        return ""  # Return an empty string if there's no valid response

def organize_paragraphs_by_subject_matter(input_html_path, output_html_path):
    # Load the input HTML file's content
    with open(input_html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    cleaned_html_content = remove_breaks_within_speaker_text(html_content)

    # Split the HTML content into manageable segments
    segments = split_html_content(cleaned_html_content)

    # Process each segment in parallel using ThreadPoolExecutor
    combined_result = ""
    with ThreadPoolExecutor() as executor:
        # Submit all tasks and store future objects in a list
        futures = [executor.submit(process_segment_with_chat, segment) for segment in segments]
        # Ensure results are processed in the order they were submitted
        for future in futures:
            combined_result += future.result()

    # Remove any "`" characters or excessive breaks
    # (just in case if ChatGBT makes any mistakes)
    final_result = combined_result.replace('`', '')
    final_result = final_result.replace('<br/><br/>', '<br/>')

    # Write the combined result to an output HTML file
    with open(output_html_path, 'w', encoding='utf-8') as file:
        file.write(final_result)

# if __name__ == '__main__':
#    input_html_path = "reformat.html"
#    output_html_path = "aiReformat.html"

    # This is the function that you want to call from api.py
#    organize_paragraphs_by_subject_matter(input_html_path, output_html_path)

    # Calculate runtime of program
#    end_time = time.time()
#    total_seconds = end_time - start_time

    # Convert total seconds to minutes and seconds
#    minutes = total_seconds // 60
#    seconds = total_seconds % 60

    # Print the runtime in minutes and seconds
#   print(f"Runtime of the AI formatting is {int(minutes)} minutes and {int(seconds)} seconds")