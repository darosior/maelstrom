

class Account:
    """The class to manage the user account.
    The methods to interact with the node will be placed here
    """

    def __init__(self):
        # Node spec
        self.host = ''
        self.key = ''
        self.balance = 0# The balance is in Satoshis