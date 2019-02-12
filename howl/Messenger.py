class Messenger:
    """Abstract class to send and receive messages
    """

    @staticmethod
    def is_valid_message(message):
        """Abstract method to check a string of invalid chars, which can not be escaped
        """

    @staticmethod
    def is_valid_recipient(recipient):
        """Abstract method to check a string of invalid chars, which can not be escaped
        """

    @staticmethod
    def is_valid_inbox(inbox):
        """Abstract method to check a string of invalid chars, which can not be escaped
        """

    def lookup(self, recipient, auth):
        """Abstract method to perform to lookup a recipient and returns it internal representation
        To be implemented by all children
        Returns an id which can be used to identify a user
        """
    def connect(self, endpoint=None):
        """Abstract method to perform the authentication and session handling with a service.
        To be implemented by all children
        Returns an auth object, to be passed onto all remote methods
        """

    @staticmethod
    def encode_message(message):
        """Abstract method to encode a message so it can be safely handed by the service
        To be implemented by all children
        Returns an id which can be used to identify a user
        """
    @staticmethod
    def decode_message(message):
        """Abstract method to decode a message so it can be safely handed by the service
        To be implemented by all children
        Returns an id which can be used to identify a user
        """

    def fetch_message(self, message_id, auth):
        """Abstract method to receive a single message
        To be implemented by all children
        Needs an auth object!
        """

    def get_inbox(self, inbox, auth):
        """Abstract method to list all messages in a given Inbox
        To be implemented by all children
        """


    def deliver_message(self, payload, recipient, auth):
        """Abstract method to perform the actual sending of a message.
        To be implemented by all children
        Needs an auth object!
        """


    def send_message(self, message, recipient):
        assert self.is_valid_recipient(recipient), "Recipient invalid!"
        assert self.is_valid_message(message), "Message contains invalid content!"

        auth = self.connect()

        recipient_id = self.lookup(recipient, auth)
        payload = self.encode_message(message)

        message_id = self.deliver_message(payload, recipient_id, auth)

        return message_id

    def receive_messages(self, inbox=None):
        assert self.is_valid_inbox(inbox)

        auth = self.connect()

        for encoded_msg in  self.get_inbox(inbox, auth):
            yield self.decode_message(encoded_msg)
