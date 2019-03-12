import os
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
Builder.load_file('ui/login.kv')


class Login(GridLayout):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        super(Login, self).__init__(**kwargs)

    def connect(self):
        """
        A call to the interface manager, to setup connection to c-simple server
        """
        try:
            node_cert = self.manager.app.receive_cert(self.ids.node_cert.text)
            with open(self.manager.app.node_cert, 'wb') as f:
                f.write(node_cert)
            self.manager.connect()
        except Exception as e:
            print(str(e))
            # TODO : display an error message here
            pass

    def new_certs(self):
        """
        Brand new certs
        """
        if os.path.isfile(self.manager.app.node_cert):
            os.path.remove(self.manager.app.node_cert)
        self.manager.app.account.gen_certificate()
        # Sends the new cert to pixeldrain
        self.manager.show_login()
