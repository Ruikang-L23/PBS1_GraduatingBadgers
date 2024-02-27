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

input_file = "CaptionSamples/Sample1/2BAW0101HDST.scc"
output_file = "sample1_scc.html"

scc_to_html(input_file, output_file)
