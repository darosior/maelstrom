from rpyc.utils import factory
from rpyc.core.service import VoidService, MasterService, FakeSlaveService
from rpyc.core.stream import SocketStream
import rpyc
import ssl, os, socket
import time

def ssl_connect(host, port, server_cert, client_cert, client_key, family=socket.AF_INET, socktype = socket.SOCK_STREAM, proto = 0):
    #context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = False
    context.load_verify_locations(server_cert)

    context.load_cert_chain(certfile = client_cert, keyfile = client_key)

    family, socktype, proto, _, sockaddr = socket.getaddrinfo(host, port, family, socktype, proto)[0]
    s = socket.socket(family, socktype, proto)
    s.settimeout(3)
    s.connect(sockaddr)
    s2 = ssl.wrap_socket(s, do_handshake_on_connect = False, server_side = False, ssl_version=ssl.PROTOCOL_TLSv1_2, certfile = client_cert, keyfile = client_key)
    try:
        s2.do_handshake()
    except ssl.SSLError as e:
        print(e)
    return factory.connect_stream(SocketStream(s2), service = VoidService)

c = ssl_connect('192.168.1.7', 8002, os.path.abspath('../c-simple/certs/node.crt'),
            os.path.abspath('../c-simple/certs/client.crt'), os.path.abspath('../c-simple/certs/client.key'))

print(c.root.get_balance())
i = c.root.gen_invoice(1000, 111111, "aa")['bolt11']
print(i)
print(c.root.decode_invoice(i))
print(c.root.get_fees(i))
print(c.root.pay(i))

