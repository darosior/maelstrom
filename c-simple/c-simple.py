from OpenSSL import crypto
import sys
import os
import time

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
        # The server's certificate
        self.pk = self.createKeyPair(crypto.TYPE_RSA, 4096)
        cert_req = self.createCertRequest(self.pk, 'sha256', C='BI', ST='Bitcoin', L='Lightning',\
                                          O='C-lightning', OU='c-simple')
        self.cert_server = self.createCertificate(cert_req, (None, self.pk), 1000, (int(time.time()), int(time.time())+365*24*3600))
        with open(os.path.join(self.settings.get('certdir'), 'node.crt'), 'w') as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, self.cert_server).decode())
            f.close()
        with open(os.path.join(self.settings.get('certdir'), 'node.key'), 'w') as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, self.pk).decode())
            f.close()

        # The client's certificate
        pk = self.createKeyPair(crypto.TYPE_RSA, 4096)
        cert_req = self.createCertRequest(pk)
        self.cert_client = self.createCertificate(cert_req, (None, pk), 1000, (int(time.time()), int(time.time())+365*24*3600))
        with open(os.path.join(self.settings.get('certdir'), 'client.crt'), 'w') as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, self.cert_client).decode())
            f.close()

    # Taken from https://github.com/pyca/pyopenssl/blob/master/examples/certgen.py
    @staticmethod
    def createKeyPair(type, bits):
        """
        Create a public/private key pair.
        Arguments: type - Key type, must be one of TYPE_RSA and TYPE_DSA
                   bits - Number of bits to use in the key
        Returns:   The public/private key pair in a PKey object
        """
        pkey = crypto.PKey()
        pkey.generate_key(type, bits)
        return pkey

    @staticmethod
    def createCertRequest(pkey, digest="sha256", **name):
        """
        Create a certificate request.
        Arguments: pkey   - The key to associate with the request
                   digest - Digestion method to use for signing, default is sha256
                   **name - The name of the subject of the request, possible
                            arguments are:
                              C     - Country name
                              ST    - State or province name
                              L     - Locality name
                              O     - Organization name
                              OU    - Organizational unit name
                              CN    - Common name
                              emailAddress - E-mail address
        Returns:   The certificate request in an X509Req object
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
        Arguments: req        - Certificate request to use
                   issuerCert - The certificate of the issuer
                   issuerKey  - The private key of the issuer
                   serial     - Serial number for the certificate
                   notBefore  - Timestamp (relative to now) when the certificate
                                starts being valid
                   notAfter   - Timestamp (relative to now) when the certificate
                                stops being valid
                   digest     - Digest method to use for signing, default is sha256
        Returns:   The signed certificate in an X509 object
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

a = App(sys.argv)


