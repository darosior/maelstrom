from rpyc.utils import factory

def ssl_connect:
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile = server_cert)
    context.load_cert_chain(certfile = client_cert, keyfile = client_key)
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s2 = context.wrap_socket(s, server_side = False)
    return factory.connect_stream(s2, service = FakeSlaveService)

