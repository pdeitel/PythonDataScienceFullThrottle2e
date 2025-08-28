# Fig. 18.7: speech_to_vtt.py
"""Function to convert audio to closed captions in WebVTT format."""

def speech_to_vtt(client, audio_path):
    """Converts an audio track into WebVTT captions."""

    # transcribe audio with per-segment timestamps (verbose_json)
    with open(audio_path, 'rb') as audio_file:
        vtt = client.audio.transcriptions.create(model='whisper-1',
            file=audio_file, response_format='vtt')
        
    return vtt # return the captions string


