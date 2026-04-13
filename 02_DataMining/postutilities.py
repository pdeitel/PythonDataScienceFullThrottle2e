# postutilities.py
"""Utility functions for processing PubNub twitter stream messages."""
import deepl
from geopy import ArcGIS
import keys
import preprocessor as p
import time

# tweet-preprocessor: remove @mentions, URLs and reserved words (RT/FAV)
p.set_options(p.OPT.MENTION, p.OPT.URL, p.OPT.RESERVED)

# DeepL translator — auto-detects source language, returns English
translator = deepl.Translator(keys.deepL_key)

def translate_post(text):
    """Translate text to English using DeepL, then censor profanity.

    DeepL auto-detects the source language, so no language code is needed.
    Falls back to returning the original text if translation fails for any
    reason (network error, unsupported language, empty input, etc.).

    Parameters
    ----------
    text : str
        Non-English post text.

    Returns
    -------
    str
        Translated English text, or the original
        text if translation is unavailable.
    """
    try:
        result = translator.translate_text(text, target_lang='EN-US')
        return result.text  # TextResult.text is the translated string
    except Exception:
        return text  # fall back gracefully on any translation error

def get_geocodes(post_list):
    """Geocode the 'location' string for each post dict in post_list.

    For each post, calls the free ArcGIS geocoding service to convert
    the user-supplied location string (e.g. 'London, UK') into a
    latitude and longitude, then adds 'latitude' and 'longitude' keys
    to that post's dict.

    Parameters
    ----------
    post_list : list of dict
        Each dict must have a 'location' key with a location string.

    Returns
    -------
    int
        Number of posts whose location string could not be geocoded.
    """
    print('Getting coordinates for post locations...')
    geo = ArcGIS()  # free geocoder — no API key required
    bad_locations = 0

    for post in post_list:
        processed = False
        delay = 0.1  # seconds to wait after a timeout before retrying
        while not processed:
            try:
                geo_location = geo.geocode(post['location'])
                processed = True
            except Exception:
                print('ArcGIS timed out. Waiting.')
                time.sleep(delay)
                delay += 0.1

        if geo_location:
            post['latitude'] = geo_location.latitude
            post['longitude'] = geo_location.longitude
        else:
            bad_locations += 1  # location string was unrecognizable

    print('Done geocoding')
    return bad_locations


##########################################################################
# (C) Copyright 2026 by Deitel & Associates, Inc. and                    #
# Pearson Education, Inc. All Rights Reserved.                           #
#                                                                        #
# DISCLAIMER: The authors and publisher of this book have used their     #
# best efforts in preparing the book. These efforts include the          #
# development, research, and testing of the theories and programs        #
# to determine their effectiveness. The authors and publisher make       #
# no warranty of any kind, expressed or implied, with regard to these    #
# programs or to the documentation contained in these books. The authors #
# and publisher shall not be liable in any event for incidental or       #
# consequential damages in connection with, or arising out of, the       #
# furnishing, performance, or use of these programs.                     #
##########################################################################
