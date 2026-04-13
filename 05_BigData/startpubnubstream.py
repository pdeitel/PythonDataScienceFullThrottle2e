# startpubnubstream.py
"""Script to receive a PubNub twitter stream, extract hashtags from posts,
   and send them to a socket for processing by Spark."""
import re
import socket
import sys

import keys
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


class TweetSubscriberCallback(SubscribeCallback):
    """Receives messages from PubNub and extracts hashtags."""

    def __init__(self, connection, limit=1000):
        """Create instance variables for tracking number of messages."""
        self.connection = connection
        self.tweet_count = 0
        self.TWEET_LIMIT = limit
        super().__init__()

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            print('Subscribed')
        elif status.category == PNStatusCategory.PNAcknowledgmentCategory:
            print('Unsubscribed')

    def message(self, pubnub, message):
        """Called when a message arrives on the channel."""
        text = message.message.get('text', '')

        # extract hashtags using regex — re.UNICODE ensures \w matches
        # letters/digits from all Unicode scripts (Arabic, CJK, Cyrillic, etc.)
        hashtags = [tag.lower() for tag in re.findall(r'#(\w+)', text, re.UNICODE)]

        if not hashtags:
            return  # skip posts with no hashtags

        hashtags_string = ' '.join(hashtags) + '\n'
        print(f'{hashtags_string}', end='')

        self.tweet_count += 1

        # send hashtags to listening Spark app
        try:
            self.connection.send(hashtags_string.encode('utf-8'))
        except Exception as e:
            print(f'Error: {e}')

        # if TWEET_LIMIT is reached, unsubscribe and stop
        if self.tweet_count == self.TWEET_LIMIT:
            print('TWEET_LIMIT reached. Application terminating.')
            pubnub.unsubscribe_all()
            sys.exit(0)


if __name__ == '__main__':
    tweet_limit = int(sys.argv[1] if len(sys.argv) > 1 else 1000)

    client_socket = socket.socket()  # create a socket

    # app will use localhost (this computer) port 9876
    client_socket.bind(('localhost', 9876))

    print('Waiting for connection')
    client_socket.listen()  # wait for client to connect

    # when connection received, get connection/client address
    connection, address = client_socket.accept()
    print(f'Connection received from {address}')

    # configure PubNub with the pubnub-twitter sample stream
    config = PNConfiguration()
    config.subscribe_key = 'sub-c-d00e0d32-66ac-4628-aa65-a42a1f0c493b'
    config.user_id = keys.pubnub_user_id  # required in SDK 6.x

    # create PubNub client and register the callback
    pubnub = PubNub(config)
    pubnub.add_listener(
        TweetSubscriberCallback(connection=connection, limit=tweet_limit))

    # subscribe to pubnub-twitter channel and begin streaming
    pubnub.subscribe().channels('pubnub-twitter').execute()


##########################################################################
# (C) Copyright 2023 by Deitel & Associates, Inc. and                    #
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
