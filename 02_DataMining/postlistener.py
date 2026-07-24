# postlistener.py
"""PubNub SubscribeCallback subclass that displays incoming post."""
from better_profanity import profanity
import threading
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
import postutilities

# load censored words list
profanity.load_censor_words()

class PostListener(SubscribeCallback):
    """Receives PubNub simulated social-media posts and displays them.

    English posts are censored before display. Non-English posts  
    are shown in their original language, followed by a censored 
    English translation via DeepL.
    """

    def __init__(self, limit=10):
        """Configure the PostListener."""
        self.post_count = 0
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
        username = post.get('user', {}).get('screen_name', 'unknown')
        lang = post.get('lang', '')
        text = post.get('text', '')

        if lang and not lang.startswith('en'):
            # show original text then the English translation
            print(f'{username} ({lang}):')
            print(f'  ORIGINAL:   {text}')
            translated_censored = profanity.censor(
                postutilities.translate_post(text))
            print(f'  TRANSLATED: {translated_censored}\n')
        else:
            # English — censored
            print(f'{username} ({lang}): {profanity.censor(text)}\n')

        self.post_count += 1
        
        if self.post_count == self.POST_LIMIT:
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
