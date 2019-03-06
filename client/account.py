from rpyc.utils import factory
from rpyc.core.service import VoidService, MasterService, FakeSlaveService
from rpyc.core.stream import SocketStream
from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import datetime
import hashlib
import os
import socket
import ssl
import time
import rpyc

class Account:
    """
    The class to manage the user account.

    Contains methods to interact with the node, most of them are just wrappers of c-simple's.
    """

    def __init__(self, node_cert=None, client_cert=None, client_key=None):
        self.balance = 0 # The balance is in Satoshis
        self.node_cert = node_cert
        self.client_cert = client_cert
        self.client_key = client_key
        if not (os.path.isfile(self.client_key) and os.path.isfile(self.client_cert)):
            self.gen_certificate(key_length=4096)
        self.conn = None

    def gen_certificate(self, key_length=4096):
        """
        Generates the client certificate
        """
        key = rsa.generate_private_key(public_exponent=65537, key_size=key_length, backend=default_backend())
        with open(self.client_key, 'wb') as f:
            f.write(key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption()))

        subject = issuer = x509.Name([])
        cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.datetime.utcnow()
            ).not_valid_after(
                datetime.datetime.utcnow() + datetime.timedelta(days=365)
            ).sign(key, hashes.SHA256(), default_backend())
        with open(self.client_cert, 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

    def connect(self, host, port=8002):
        """
        Setup connection to the node via a secure socket.

        :param host: the node ip.
        :param port: the port behind which c-simple server runs, default is 8002.
        """
        # To avoid trying to connect without anything set up.
        if not (os.path.isfile(self.client_cert) and os.path.isfile(self.client_key)):
            self.gen_certificate(key_length=4096)
        if not os.path.isfile(self.node_cert):
            raise Exception('Server certificate is missing. Cannot initiate the connection')
        try:
            # Connecting the socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(1)
            s.connect((host, port))

            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_verify_locations(self.node_cert)
            context.load_cert_chain(self.client_cert, self.client_key)

            secure_sock = context.wrap_socket(s, server_side=False, server_hostname=host)
            self.conn = factory.connect_stream(SocketStream(secure_sock), service=VoidService)

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

    def pay(self, bolt11, description='', amount=None):
        """
        Pays the specified invoice.

        :param bolt11: The invoice to pay.
        :param amount: The amount to pay, needed if not included in the invoice.
        :param description: The payment description.
        :return: True if payment was completed, False otherwise.
        """
        status = self.conn.root.pay(bolt11, description, amount)
        print(status)
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

        :param amount: Payment value in mili satoshis.
        :param label: Unique string or number (treated as a string : '01' != '1')
        :param desc: A description for the payment.

        :returns: The invoice
        """
        if not label:
            label = hashlib.sha256(str(time.time()).encode()).hexdigest()
        if not desc:
            desc = str(time.time())
        return self.conn.root.gen_invoice(amount, label, desc)

    def decode_invoice(self, invoice):
        """
        Decodes the specified invoice (as a BOLT11 str).

        :param invoice: The invoice to decode.
        :return: Decoded invoice, as a dict.
        """
        return self.conn.root.decode_invoice(invoice)
