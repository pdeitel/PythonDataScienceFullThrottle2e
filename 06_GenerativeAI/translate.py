# Fig. 18.2: translate.py
"""Function used to translate text to specified language."""

def translate(client, text, language):
    """Translate text into the specified language using the 
    OpenAI Responses API and return the translation."""

    instructions = f"""You are an expert in natural language translation.
        Translate the input text into {language}."""
    
    response = client.responses.create(model='gpt-5-mini',
        instructions=instructions, input=text)
    
    return response.output_text
