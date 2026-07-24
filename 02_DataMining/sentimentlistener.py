# sentimentlistener.py
"""PubNub SubscribeCallback that tallies positive, neutral and negative post sentiments."""
from better_profanity import profanity
import threading
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from textblob import TextBlob
import postutilities

# load censored words list
profanity.load_censor_words()

class SentimentListener(SubscribeCallback):
    """Receives PubNub twitter stream messages and performs sentiment analysis.

    Non-English posts are translated to English with DeepL before analysis.
    Sentiment is always scored against English text so results are consistent
    regardless of the original post language.
    """

    def __init__(self, sentiment_dict, limit=100):
        """Configure the SentimentListener.

        Parameters
        ----------
        sentiment_dict : dict
            Dict with keys 'positive', 'neutral', 'negative' to tally counts.
        limit : int
            Number of non-retweet posts to process before stopping.
        """
        self.sentiment_dict = sentiment_dict
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

        # skip reposts — their text is someone else's and skews analysis
        if post.get('text', '').startswith('RT'):
            return

        lang = post.get('lang', '')
        text = post.get('text', '')

        if lang and not lang.startswith('en'):
            # translate to English for consistent sentiment scoring
            english_text = postutilities.translate_post(text)
            show_original = True
        else:
            english_text = text
            show_original = False

        if not english_text.strip():
            return  # skip if nothing remains after cleaning/translation

        # classify sentiment with TextBlob (always on English text)
        blob = TextBlob(english_text)
        if blob.sentiment.polarity > 0.1:
            self.sentiment_dict['positive'] += 1
            sentiment = '+'
        elif blob.sentiment.polarity < -0.1:
            self.sentiment_dict['negative'] += 1
            sentiment = '-'
        else:
            self.sentiment_dict['neutral'] += 1
            sentiment = ' '

        username = post.get('user', {}).get('screen_name', 'unknown')

        if show_original:
            print(f'{sentiment} {username} ({lang}):')
            print(f'  ORIGINAL:   {text}')
            print(f'  TRANSLATED: {profanity.censor(english_text)}\n')
        else:
            print(f'{sentiment} {username}: {profanity.censor(english_text)}\n')

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
