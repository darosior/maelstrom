from rpyc.utils import factory
from rpyc.core.service import VoidService, MasterService, FakeSlaveService
from rpyc.core.stream import SocketStream
import rpyc
import os
import ssl, socket
import time
import hashlib

class Account:
    """
    The class to manage the user account.
    
    Contains methods to interact with the node, most of them are just wrappers of c-simple's.
    """

    def __init__(self):
        self.balance = 0 # The balance is in Satoshis
        self.server_cert = None
        self.client_cert = None
        self.client_key = None
        self.conn = None
        
    def connect(self, host, port=8002):
        """
        Setup connection to the node via a secure socket.
        
        :param host: the node ip.
        :param port: the port behind which c-simple server runs, default is 8002.
        """
        # To avoid trying to connect without anything set up.
        if not (self.server_cert and self.client_cert and self.client_key):
            raise
        try:
            # Creating the SSL context
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=self.server_cert)
            # Connecting the socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            s.connect((host, port))
            # Wrapping it to then get the secure connnection
            s2 = ssl.wrap_socket(s, do_handshake_on_connect = False, server_side = False, ssl_version=ssl.PROTOCOL_TLSv1_2, certfile = client_cert, keyfile = client_key)
            s2.do_handshake()
            self.conn = factory.connect_stream(SocketStream(s2), service = VoidService)
        except ssl.SSLError as e:
            raise Exception('Could not connect to host {}:{}, getting following ssl error :\n{}'.format(host, port, e))
    
    def get_balance(self, network='all'):
        """
        Fetch the balance from the node.
        
        :param where: Which network's balance should be returned. Possible values : 'all', 'bitcoin', 'lightning'.
        :return: Balance in satoshis if network == 'lightning' or network == 'bitcoin'. Else a dict with every balance.
        """
        balances = self.conn.root.get_balance()
        if network == 'lightning':
            return sum([balances['onchannel'][i] for i in balances['onchannel']])
	    elif network == 'bitcoin':
	        return sum([balances['onchain'][i] for i in balances['onchain']])
	    else:
	        return balances
	
	def pay(self, invoice, amount=None):
	    """
	    Pays the specified invoice.
	    
	    :param invoice: The invoice to pay.
        :param amout: The amount to pay, needed if not included in the invoice.
        :return: True if payment was completed, False otherwise. 
	    """
	    status = self.conn.root.pay(invoice, amount)
	    if status == 'complete':
	        return True
	    else:
	        return False
	
	def get_fees(self, invoice, amount=None):
	    """
	    Calculates fees needed to pay a specified invoice.
	    
	    :param invoice: The invoice to pay.
        :param amout: The amount to pay, needed if not included in the invoice.
        :return: The fees (in msatoshis)
	    """
	    return self.conn.route.get_fees(invoice, amount=None)
	    
	def gen_invoice(self, amount, label=None, desc=None):
	    """
	    Generates an invoice for being paid.
	    
	    :param msatoshi: Payment value in mili satoshis.
	    :param label: Unique string or number (treated as a string : '01' != '1')
	    :param desc: A description for the payment.
	    
	    :returns: The invoice
	    """
	    if not label:
	        label = hashlib.sha256(str(time.time()).encode()).hexdigest()
	    return self.conn.root.gen_invoice(amount, label, desc)
	    	
