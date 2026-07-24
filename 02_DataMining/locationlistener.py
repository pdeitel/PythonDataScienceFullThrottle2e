# locationlistener.py
"""PubNub SubscribeCallback that collects posts with user location strings for mapping."""
from better_profanity import profanity
import threading
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
import postutilities

# load censored words list
profanity.load_censor_words()

class LocationListener(SubscribeCallback):
    """Collects PubNub posts whose sender has a non-empty user location string.

    Non-English post text is translated to English with DeepL so the map
    popup always displays readable text regardless of the original language.
    """

    def __init__(self, counts_dict, posts_list, limit=50):
        """Configure the LocationListener.

        Parameters
        ----------
        counts_dict : dict
            Dict with keys 'total_posts' and 'locations' to track progress.
        posts_list : list
            List to which located post dicts are appended.
        limit : int
            Number of located posts to collect before stopping.
        """
        self.counts_dict = counts_dict
        self.posts_list = posts_list
        self.POST_LIMIT = limit
        self.done = threading.Event()  # set when POST_LIMIT is reached
        super().__init__()

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            print('Connected to PubNub twitter stream')
        elif status.category == PNStatusCategory.PNAcknowledgmentCategory:
            print('Unsubscribed')

    def message(self, pubnub, message):
        """Called each time a new post arrives on the channel."""
        if self.done.is_set():
            return  # ignore messages buffered after POST_LIMIT was reached
        post = message.message
        self.counts_dict['total_posts'] += 1

        # use the user-supplied location string from the sender's profile
        location = post.get('user', {}).get('location', '')
        if not location:
            return  # skip posts with no user location

        self.counts_dict['locations'] += 1
        username = post.get('user', {}).get('screen_name', 'unknown')
        lang = post.get('lang', '')
        text = post.get('text', '')

        # translate non-English post text so map popups are always readable
        if lang and not lang.startswith('en'):
            english_text = postutilities.translate_post(text)
        else:
            english_text = text

        english_text = profanity.censor(english_text)
        
        self.posts_list.append({
            'username': username,
            'text': english_text,  # always English for the map popup
            'location': location   # geocoded later by get_geocodes()
        })

        print(f"{self.counts_dict['locations']:3}: {username} — {location}")

        if self.counts_dict['locations'] == self.POST_LIMIT:
            pubnub.unsubscribe_all()
            self.done.set()  # signal completion to the notebook


##########################################################################
# (C) Copyright 2025 by Deitel & Associates, Inc. and                    #
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
