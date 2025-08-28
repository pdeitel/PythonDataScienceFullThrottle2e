# Fig. 18.3: speech_to_text.py
"""Function used to transcribe speech to text."""

def speech_to_text(client, audio_path):
    """Transcribes the audio file at audio_path to text."""
    
    with open(audio_path, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create( 
            model='gpt-4o-transcribe', file=audio_file)
        
    return transcript.text 