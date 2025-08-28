# Fig. 18.5: create_image.py
"""Function used to create original images."""

import base64

def create_image(client, path, prompt):
    """Generates an original image based on the prompt and
    stores it in the file specified by path."""
    image = client.images.generate(model='gpt-image-1', prompt=prompt)

    # decode Base64-encoded image bytes
    image_bytes = base64.b64decode(image.data[0].b64_json)

    # output bytes to path
    path.write_bytes(image_bytes) 
    print(f'Image stored in:\n{path}')


