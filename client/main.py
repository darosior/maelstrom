# Kivy imports
import kivy
kivy.require('1.10.1')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.base import EventLoop
# UI screens imports
from home import Home
from login import Login
from pay import Pay
from scan import Scan
from request_payment import RequestPayment
from account import Account
# Other dependencies
import os
import re
import requests


class InterfaceManager(BoxLayout):
    def __init__(self, app, **kwargs):
        self.app = app
        # To avoid a long loading at app launch, we initialize the screens at None
        # and then we affect them dinamically (if not self.screen : self.screen = Screen(self))
        self.login = Login(self)
        self.home = None
        self.pay_widget = None
        self.scan_widget = None
        self.request_payment = None
        super(InterfaceManager, self).__init__(**kwargs)

    def show_login(self):
        """
        Shows the login "page".
        """
        self.clear_widgets()
        try:
            cert_id = self.app.send_cert()
            self.login.ids.client_cert.text = 'Enter the following number on the node : ' + cert_id
        except Exception as e:
            # There was a problem with cert upload, wether there is no connection or certificates are corrupted
            self.login.ids.client_cert.text = '[color=ff3333]' + str(e) + '[/color]'
            # So we add the possibility to the user to re-generate them
            self.login.ids.connect.text = '[color=ff3333]Generate new certificates[/color]'
            self.login.ids.connect.on_release = self.login.new_certs
        self.add_widget(self.login)

    def show_home(self):
        """
        Shows the homepage
        """
        if not self.home:
            self.home = Home(self)
        self.clear_widgets()
        self.add_widget(self.home)

    def show_pay(self):
        """
        Shows the payment page.
        """
        if not self.pay_widget:
            self.pay_widget = Pay(self)
        self.clear_widgets()
        self.add_widget(self.pay_widget)
        self.pay_widget.ids.payment_details.text = ''

    def show_scan(self):
        """
        Shows the scan page
        """
        if not self.scan_widget:
            self.scan_widget = Scan(self)
            self.scan_widget.ids.zbarcam.ids.xcamera._camera.start()
        self.clear_widgets()
        self.add_widget(self.scan_widget)

    def show_request_payment(self):
        """
        Shows the request payment page
        """
        if not self.request_payment:
            self.request_payment = RequestPayment(self)
        self.clear_widgets()
        self.add_widget(self.request_payment)

    def connect(self):
        """
        Set up the connection to the c-simple server.
        Checks the certfiles extensions and then calls the connect method from the "Account" class, which speaks to
        c-simple.
        """
        # Default port value is 8002
        port = self.login.ids['port'].text if self.login.ids['port'].text else '8002'
        ip = self.login.ids['ip'].text.replace(' ', '')
        try:
            self.app.account.connect(ip, int(port))
            if not self.home:
                self.home = Home(self)
            self.home.update_balance_text()
            self.show_home()
            # If connection succeeded, we store the config for next time
            self.app.config.setall('connection', {
                'cert_dir': self.app.cert_dir,
                'ip': ip,
                'port': port,
            })
            self.app.config.write()
        except Exception as e:
            if 'Connection refused' in str(e):
                self.login.ids['error'].text = 'Connection refused at {}:{}.'.format(self.login.ids['ip'].text, port)
            elif 'Invalid argument' in str(e) or 'No route to host' in str(e):
                self.login.ids['error'].text = 'Wrong values for ip and/or port.'
            else:
                self.login.ids['error'].text = str(e) # ^^


class Csimple(App):
    def __init__(self, **kwargs):
        super(Csimple, self).__init__(**kwargs)
        self.config = self.load_config()
        self.interface_manager = InterfaceManager(self, orientation='vertical')
        # The certificates stuff
        if os.path.isdir(self.config.get('connection', 'cert_dir')):
            self.cert_dir = self.config.get('connection', 'cert_dir')
        else:
            self.cert_dir = os.path.join(os.path.dirname(__file__), 'certs')
        if not os.path.isdir(self.cert_dir):
            os.makedirs(self.cert_dir)
        self.client_cert = os.path.join(self.cert_dir, 'client.pem')
        self.client_key = os.path.join(self.cert_dir, 'client.key')
        self.node_cert = os.path.join(self.cert_dir, 'node.pem')
        ip = self.config.get('connection', 'ip')
        port = int(self.config.get('connection', 'port'))
        # The interface to c-simple running on the node
        self.account = Account(self.client_cert, self.client_key, self.node_cert)
        # ..And trying to connect if nothing changed, so the user doesn't set the parameters again
        try:
            EventLoop.window.bind(on_keyboard=self.key_input)
            self.account.connect(ip, port)
            self.interface_manager.home.update_balance_text()
            self.interface_manager.show_home()
        except Exception as e:
            self.interface_manager.login.text = str(e)
            self.interface_manager.show_login()

    def build(self):
        return self.interface_manager

    def build_config(self, config):
        if self.config.has_section('connection'):
            self.config.read(self.get_application_config())
        else:
            self.config.add_section('connection')
            self.config.setall('connection', {
                'cert_dir': 'certs',
                'ip': '',
                'port': '8002',
            })
            self.config.write()

    def key_input(self, window, key, scancode, codepoint, modifier):
        """
        Overrides the back button (escape on desktop) default behaviour
        """
        if key == 27:
            # If already on the home screen, we close the app
            if hasattr(self.interface_manager.children[0], 'name'):
                if self.interface_manager.children[0].name in ('home', 'login'):
                    self.stop()
            # Otherwise we show the home screen (since it is the parent screen of every screens)
            self.interface_manager.show_home()
            return True # Stop propagation
        return False

    def send_cert(self):
        """
        Sends the certificate to pixeldrain in order to make the handshake
        :return: The id of the certificate on pixeldrain.
        """
        with open(self.client_cert, 'rb') as f:
            file_content = f.read()
        r = requests.post('https://pixeldrain.com/api/upload', files={'file':file_content}).json()
        if r.get('success'):
            return r.get('id')
        raise Exception('Could not upload the certificate to pixeldrain')

    def receive_cert(self, id):
        """
        Receive a cert from pixeldrain.
        :param id: The id of the certificate on pixeldrain.
        :return: The data of the certificate (the file content).
        """
        r = requests.get('https://pixeldrain.com/api/file/'+str(id))
        if r.status_code == 200:
            return r.content #bytes
        raise Exception('Could not receive the file with id '+str(id)+' from pixeldrain')

    def btc_usd(self):
        """
        Fetch the bitcoin price in USD from blockchain.info
        :return: (int) the price in USD
        """
        price = requests.get('https://blockchain.info/ticker').json()['USD']['last']
        return int(price)

    def to_usd(self, satoshis):
        """
        Converts a given value in satoshis to usd
        :param satoshis: (int) The number of satoshis
        :return: (int) The price in USD
        """
        return satoshis*self.btc_usd()/100000000

if __name__ == '__main__':
    Csimple().run()
