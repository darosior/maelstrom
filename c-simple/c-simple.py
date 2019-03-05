import sys
import os
import time
import argparse
import datetime
from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from sslauthenticator import SSLAuthenticator
from rpyc.utils.server import ThreadedServer
from lightningservice import LightningService

class App:
    """The main class."""

    def __init__(self):
        # Parsing command-line arguments, check for needed directories
        self.args = self.parse_arguments()
        if not os.path.isdir(self.args.certdir):
            print('The certificates directory isn\'t reconized, creating it. ({})'.format(self.args.certdir))
            os.makedirs(self.args.certdir)
        if not os.path.isdir(self.args.lndir):
            print(self.args.lndir)
            raise Exception('Couldn\'t open the lightning directory specified. (default is ~/.lightning)')
        
        print('Checking server certificate and key.. ', end='')
        self.node_cert = os.path.join(self.args.certdir, 'node.pem')
        self.node_key = os.path.join(self.args.certdir, 'node.key')
        if not os.path.isfile(self.node_cert) or not os.path.isfile(self.node_key) or self.args.newcerts:
            print('Generating new ones..')
            self.gen_certificate(4096, self.node_cert, self.node_key)
        print('OK')

        print('Checking client certificate.. ', end='')
        self.client_cert = os.path.join(self.args.certdir, 'client.pem')
        if not os.path.isfile(self.client_cert):
            print('Client certificate is not present in the certificates directory. Please provide it *somehow*.')
            exit(1)
        print('OK')

    def run(self):
        """
        Starts the RPyC server.
        """
        print('Setting up the server ..')
        auth = SSLAuthenticator(self.node_key, self.node_cert, ca_certs=self.client_cert)
        server = ThreadedServer(LightningService, port=int(self.args.port), authenticator=auth, protocol_config={"allow_all_attrs": True})
        print('Server started and listening on {}:{}'.format(self.args.interface, self.args.port))
        server.start()

    @staticmethod
    def parse_arguments():
        """
        Parses command line arguments with argparse.

        :return: An object containing all arguments and their value.
        """
        parser = argparse.ArgumentParser(description='Setup a server to connect to remotly access your lightning node.')
        parser.add_argument('-i', '--interface', default='127.0.0.1',
                            help='The interface to run the server on. If set to 0.0.0.0, it will be remotely accessible',
                            dest='interface')
        parser.add_argument('-p', '--port', default='8002', help='Sets the port for the server to be starting on',
                            dest='port')
        parser.add_argument('-c', '--certdir', default='./certs', help='The directory to put the certificates in.',
                            dest='certdir')
        parser.add_argument('-g', '--new-certs', help='If specified, new certificate will be generated',
                            dest='newcerts', action='store_true', default=False)
        parser.add_argument('-l', '--lightning-dir', default=os.path.join(os.path.expanduser('~'),'.lightning/'),
                            help='Specifies the lightning directory', dest='lndir')
        parser.add_argument('-lc', '--lightning-conf', help='If set, specifies the conf used by c-lightning',
                            dest='lnconf')
        return parser.parse_args()

    @staticmethod
    def gen_certificate(key_length, filename_cert, filename_key):
        """Generates the server certificate.
        :param key_length: The length of the RSA key to use.
        :param filename_cert: The file to which the certificate will be stored.
        :param filename_key: The file to which the private key will be stored.
        """
        # We generate and store the private key.
        key = rsa.generate_private_key(public_exponent=65537, key_size=key_length, backend=default_backend())
        with open(filename_key, 'wb') as f:
            f.write(key.private_bytes(encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL, 
                encryption_algorithm=serialization.NoEncryption()))

        # We generate and store the certificate.
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
        with open(filename_cert, 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
   

if __name__ == '__main__':
    app = App()
    app.run()

