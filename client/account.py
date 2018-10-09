from rpyc.utils import factory
from rpyc.core.service import VoidService, MasterService, FakeSlaveService
from rpyc.core.stream import SocketStream
import rpyc
import ssl, os, socket
import time

class Account:
    """The class to manage the user account.
    
    The methods to interact with the node will be placed here.
    """

    def __init__(self):
        self.balance = 0 # The balance is in Satoshis
        self.server_cert = None
        self.client_cert = None
        self.client_key = None
        
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
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
            # Connecting the socket
            family, socktype, proto, _, sockaddr = socket.getaddrinfo(host, port, family, socktype, proto)[0]
            s = socket.socket(family, socktype, proto)
            s.connect(sockaddr)
            # Wrapping it to then get the secure connnection
            s2 = ssl.wrap_socket(s, do_handshake_on_connect = False, server_side = False, ssl_version=ssl.PROTOCOL_TLSv1_2, certfile = client_cert, keyfile = client_key)
            s2.do_handshake()
            self.connection = factory.connect_stream(SocketStream(s2), service = VoidService)
        except ssl.SSLError as e:
            raise Exception('Could not connect to host {}:{}, getting following ssl error :\n{}'.format(host, port, e))
            
                    
        
