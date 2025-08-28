# Fig. 18.4: text_to_speech.py
"""Function used to synthesize speech from text."""

def text_to_speech(client, text, path, voice, instructions=''):
    """Synthesizes speech from the provided text and 
    writes it to the file specified by path."""
    response = client.audio.speech.create(model='gpt-4o-mini-tts',
        voice=voice, input=text, instructions=instructions)

    response.write_to_file(str(path))