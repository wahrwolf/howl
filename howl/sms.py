from twilio.rest import Client
from twilio.rest.api.v2010.account.message import MessageInstance
from .Messenger import Messenger

class TwilioSMS(Messenger):

    def __init__(self, account, token, number=None):
        self.__account_id = account
        self.__token = token

        self.__number = number

    @staticmethod
    def is_valid_message(message):
        """All strings can be send!
        """
        return isinstance(message, str)

    @staticmethod
    def is_valid_recipient(recipient):
        """Currently only true phone numbers (as int) are allowed
        """
        return isinstance(recipient, str)


    @staticmethod
    def is_valid_inbox(inbox):
        """We do not allow any inbox (except None)
        """
        return isinstance(inbox,str) or inbox is None

    def lookup(self, recipient, auth):
        """Just mock a look up, but fail on invalid recipients
        """
        assert self.is_valid_recipient(recipient), "Invalid recipient"
        return recipient

    def connect(self, endpoint=None):
        """Abstract method to perform the authentication and session handling with a service.
        To be implemented by all children
        Returns an auth object, to be passed onto all remote methods
        """
        return Client(self.__account_id, self.__token)


    @staticmethod
    def encode_message(message):
        """Abstract method to encode a message so it can be safely handed by the service
        To be implemented by all children
        Returns an id which can be used to identify a user
        """
        return ''.join([i if ord(i) < 128 else '?' for i in message])



    @staticmethod
    def decode_message(message):
        """Abstract method to decode a message so it can be safely handed by the service
        To be implemented by all children
        Returns an id which can be used to identify a user
        """
        assert isinstance(message, MessageInstance), "Message not a valid instance!"
        return str(message.from_ + ": " + message.body)

    def fetch_message(self, message_id, auth):
        """Abstract method to receive a single message
        To be implemented by all children
        Needs an auth object!
        """
        return auth.messages(message_id)

    def get_inbox(self, inbox, auth):
        """Abstract method to list all messages in a given Inbox
        To be implemented by all children
        """

        if inbox is None:
            inbox = self.__number

        return  auth.messages.list(to=inbox)

    def deliver_message(self, payload, recipient, auth):
        """Abstract method to perform the actual sending of a message.
        To be implemented by all children
        Needs an auth object!
        """
        auth.messages.create(
                body=payload,
                to=recipient,
                from_=self.__number)

