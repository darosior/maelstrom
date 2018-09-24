from OpenSSL import crypto
import sys

class App:
    """The main class.

    """
    def __init__(self, *args):
        # Default settings
        self.settings = {
            'host' : '127.0.0.1',
            'port' : '8002',
            'certdir' : './certs',
            'no-ssl' : 'false',
            'lightningdir' : '~/.lightning',
            'lightningconf' : ''
        }
        # Parsing arguments
        i = 0
        for arg in args:
            for setting in self.settings:
                if setting == arg[1:] or setting == arg[2:]:
                    self.settings[setting] = args[i+1]
            i += 1
        # Setting up for SSL
        print('Generating the certs..')
        self.pk = crypto.PKey()
        self.pk.generate_key(crypto.TYPE_RSA, 4096)
        self.cert_server = crypto.X509Req()
        self.cert_server.get_subject().C = ''
        self.cert_server.get_subject().ST = ''
        self.cert_server.get_subject().L = ''
        self.cert_server.get_subject().O = ''
        self.cert_server.get_subject().OU = ''
        self.cert_server.get_subject().CN = ''

a = App()


