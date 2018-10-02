from OpenSSL import crypto
import sys
import os
import time
import argparse
from sslauthenticator import SSLAuthenticator
from rpyc.utils.server import ThreadedServer
from lightningservice import LightningService

class App:
    """The main class."""

    def __init__(self):
        # Parsing command-line arguments
        self.args = self.parse_arguments()
        if not os.path.isdir(self.args.certdir):
            print('The certs directory isn\'t reconized, creating it. ({})'.format(self.args.certdir))
            try:
                os.makedirs(self.args.certdir)
            except Exception as e:
                print(e)
        if not os.path.isdir(self.args.lndir):
            print(self.args.lndir)
            raise Exception('Couldn\'t open the lightning directory specified. (default is ~/.lightning)')
        if self.args.nossl:
            print('Starting the server without ssl, be carefull of what information is transmitted and on which network..')

        # Setting up certificates for SSL
        print('Checking the certs..')

        # The server's certificate
        if not os.path.isfile(os.path.join(self.args.certdir, 'node.crt')) or self.args.newcerts:
            self.pk = self.createKeyPair(crypto.TYPE_RSA, 4096)
            cert_req = self.createCertRequest(self.pk, 'sha256', C='BI', ST='Bitcoin', L='Lightning',\
                                              O='C-lightning', OU='c-simple')
            self.cert_server = self.createCertificate(cert_req, (None, self.pk), 1000,
                                                  (0, int(time.time()) + 365 * 24 * 3600))
            with open(os.path.join(self.args.certdir, 'node.crt'), 'w') as f:
                f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, self.cert_server).decode())
                f.close()
            with open(os.path.join(self.args.certdir, 'node.key'), 'w') as f:
                f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, self.pk).decode())
                f.close()
            print('A new server cert (along with a new private key) has been generated in {}'.format(self.args.certdir))
        else:
            print('A certificate is already present for the server. Start c-simple with the --new-certs argument to \
                  generate new ones.')
        self.server_certfile = os.path.abspath(os.path.join(self.args.certdir, 'node.crt'))
        self.server_keyfile = os.path.abspath(os.path.join(self.args.certdir, 'node.key'))

        # The client's certificate
        if not os.path.isfile(os.path.join(self.args.certdir, 'client.crt')) or self.args.newcerts:
            pk = self.createKeyPair(crypto.TYPE_RSA, 4096)
            cert_req = self.createCertRequest(pk)
            self.cert_client = self.createCertificate(cert_req, (None, pk), 1000,
                                                      (0, int(time.time()) + 365 * 24 * 3600))
            with open(os.path.join(self.args.certdir, 'client.crt'), 'w') as f:
                f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, self.cert_client).decode())
                f.close()
            with open(os.path.join(self.args.certdir, 'client.key'), 'w') as f:
                f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pk).decode())
                f.close()
            print('A new client cert (along with a new private key) has been generated in {}'.format(self.args.certdir))
        else:
            print('A certificate is already present for the server. Start c-simple with the --new-certs argument to \
                  generate new ones.')
        self.client_certfile = os.path.abspath(os.path.join(self.args.certdir, 'client.crt'))

        # It doesn't make any sense to talk about auth if we keep this file on the serv
        print('Please copy {} on the client\'s device and delete them from the server'.format(
            os.path.abspath(os.path.join(self.args.certdir, 'client.key'))))

    def run(self):
        """
        Starts the server.

        :return:
        """
        print('\n\nSetting up the server ..\n')
        auth = SSLAuthenticator(self.server_keyfile, self.server_certfile, ca_certs=self.client_certfile)
        server = ThreadedServer(LightningService, port=int(self.args.port), authenticator=auth, protocol_config = {"allow_public_attrs" : True})
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
        parser.add_argument('-n', '--no-ssl', help='If specified, the communication won\'t be encrypted. Be carefull.',
                            dest='nossl', action='store_true', default=False)
        parser.add_argument('-g', '--new-certs', help='If specified, new certificate will be generated',
                            dest='newcerts', action='store_true', default=False)
        parser.add_argument('-l', '--lightning-dir', default=os.path.join(os.path.expanduser('~'),'.lightning/'),
                            help='Specifies the lightning directory', dest='lndir')
        parser.add_argument('-lc', '--lightning-conf', help='If set, specifies the conf used by c-lightning',
                            dest='lnconf')
        return parser.parse_args()

    # Taken from https://github.com/pyca/pyopenssl/blob/master/examples/certgen.py
    @staticmethod
    def createKeyPair(type, bits):
        """
        Create a public/private key pair.

        :argument type: - Key type, must be one of TYPE_RSA and TYPE_DSA
        :argument bits: - Number of bits to use in the key

        :return: The public/private key pair in a PKey object
        """
        pkey = crypto.PKey()
        pkey.generate_key(type, bits)
        return pkey

    @staticmethod
    def createCertRequest(pkey, digest="sha256", **name):
        """
        Create a certificate request.

        :argument pkey:   - The key to associate with the request
        :argument digest: - Digestion method to use for signing, default is sha256
        :argument **name: - The name of the subject of the request, possible
                            arguments are:
                              C     - Country name
                              ST    - State or province name
                              L     - Locality name
                              O     - Organization name
                              OU    - Organizational unit name
                              CN    - Common name
                              emailAddress - E-mail address

        :return: Certificate request in an X509Req object
        """
        req = crypto.X509Req()
        subj = req.get_subject()

        for key, value in name.items():
            setattr(subj, key, value)

        req.set_pubkey(pkey)
        req.sign(pkey, digest)
        return req

    @staticmethod
    def createCertificate(req, issuerCertKey, serial, validityPeriod, digest="sha256"):
        """
        Generate a certificate given a certificate request.

        :argument req:        - Certificate request to use
        :argument issuerCert: - The certificate of the issuer
        :argument issuerKey:  - The private key of the issuer
        :argument serial:     - Serial number for the certificate
        :argument notBefore:  - Timestamp (relative to now) when the certificate starts being valid
        :argument notAfter:   - Timestamp (relative to now) when the certificate stops being valid
        :argument digest:     - Digest method to use for signing, default is sha256

        :return: The signed certificate in an X509 object
        """
        issuerCert, issuerKey = issuerCertKey
        notBefore, notAfter = validityPeriod
        cert = crypto.X509()
        cert.set_serial_number(serial)
        cert.gmtime_adj_notBefore(notBefore)
        cert.gmtime_adj_notAfter(notAfter)
        if issuerCert is not None:
            cert.set_issuer(issuerCert.get_subject())
        cert.set_subject(req.get_subject())
        cert.set_pubkey(req.get_pubkey())
        cert.sign(issuerKey, digest)

        return cert

if __name__ == '__main__':
    app = App()
    app.run()

