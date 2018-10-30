import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from home import Home
from login import Login
from file_browser import FileBrowser
from pay import Pay
from scan import Scan
from account import Account
import re
import requests


class InterfaceManager(BoxLayout):
    def __init__(self, app, **kwargs):
        self.app = app
        self.file_chooser = FileBrowser(self)
        self.login = Login(self)
        self.home = Home(self)
        self.pay_widget = Pay(self)
        self.scan_widget = None
        # Used to determine which cert to store. Not very elegant but functional
        self.button_pressed = None
        super(InterfaceManager, self).__init__(**kwargs)

    def show_login(self):
        """
        Shows the login "page".
        """
        self.clear_widgets()
        self.add_widget(self.login)

    def show_fb(self, button_pressed):
        """
        Shows the file browser
        :param button_pressed: The button pressed to access the fb.
        """
        self.clear_widgets()
        self.button_pressed = button_pressed
        self.add_widget(self.file_chooser)

    def show_home(self):
        """
        Shows the homepage
        """
        self.clear_widgets()
        self.add_widget(self.home)

    def show_pay(self):
        """
        Shows the payment page.
        """
        # The only way to stop the camera and retrieve it later without throwing an error
        # see https://github.com/kivy/kivy/issues/3569
        if self.scan_widget:
            self.scan_widget.ids.zbarcam.ids.xcamera._camera = None
            self.scan_widget = None
        self.clear_widgets()
        self.add_widget(self.pay_widget)
        self.pay_widget.ids.payment_details.text = ''

    def show_scan(self):
        """
        Shows the scan page
        """
        # To retrieve the camera, see show_pay()
        self.scan_widget = Scan(self)
        self.scan_widget.ids.zbarcam.ids.xcamera._camera.start()
        self.clear_widgets()
        self.add_widget(self.scan_widget)

    def load_cert(self, filename):
        """
        Save the cert pathname to the application. Changes button text to show the chosen filename.
        :param filename: The path to the cert file.
        """
        if self.button_pressed == 'server cert':
            self.app.account.server_cert = filename
            # If multiple selection
            self.login.ids['server_cert'].text = re.sub(r'\([^)]*\)', '', self.login.ids['server_cert'].text)
            self.login.ids['server_cert'].text += ' ({})'.format(filename)
        elif self.button_pressed == 'client cert':
            self.app.account.client_cert = filename
            # If multiple selection
            self.login.ids['client_cert'].text = re.sub(r'\([^)]*\)', '', self.login.ids['client_cert'].text)
            self.login.ids['client_cert'].text += ' ({})'.format(filename)
        elif self.button_pressed == 'client key':
            self.app.account.client_key = filename
            # If multiple selection
            self.login.ids['client_key'].text = re.sub(r'\([^)]*\)', '', self.login.ids['client_key'].text)
            self.login.ids['client_key'].text += ' ({})'.format(filename)

    def connect(self):
        """
        Set up the connection to the c-simple server.
        Checks the certfiles extensions and then calls the connect method from the "Account" class, which speaks to
        c-simple.
        """
        if not self.app.account.server_cert or not '.crt' == self.app.account.server_cert[-4:]:
            self.login.ids['error'].text = 'Wrong file format for server certificate.'
        elif not self.app.account.client_cert or not '.crt' == self.app.account.client_cert[-4:]:
            self.login.ids['error'].text = 'Wrong file format for client certificate.'
        elif not self.app.account.client_key or not '.key' == self.app.account.client_key[-4:]:
            self.login.ids['error'].text = 'Wrong file format for client key.'
        else:
            # Default port value is 8002
            port = self.login.ids['port'].text if self.login.ids['port'].text else '8002'
            ip = self.login.ids['ip'].text.replace(' ', '')
            try:
                self.app.account.connect(ip, int(port))
                self.home.update_balance_text()
                self.show_home()
                # If connection succeeded, we stock the config for next time
                self.app.config.setall('connection', {
                    'server_cert': self.app.account.server_cert,
                    'client_cert': self.app.account.client_cert,
                    'client_key': self.app.account.client_key,
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
        # The interface to c-simple running on the node
        self.account = Account()
        # Loading the config..
        self.account.server_cert = self.config.get('connection', 'server_cert')
        self.account.client_cert = self.config.get('connection', 'client_cert')
        self.account.client_key = self.config.get('connection', 'client_key')
        # ..And trying to connect if nothing changed, so the user doesn't set the parameters again
        try:
            self.account.connect(self.config.get('connection', 'ip'), int(self.config.get('connection', 'port')))
            self.interface_manager.home.update_balance_text()
            self.interface_manager.show_home()
        except:
            self.interface_manager.show_login()


    def build(self):
        return self.interface_manager

    def build_config(self, config):
        if self.config.has_section('connection'):
            self.config.read(self.get_application_config())
        else:
            self.config.add_section('connection')
            self.config.setall('connection', {
                'server_cert': '',
                'client_cert': '',
                'client_key': '',
                'ip': '',
                'port': '8002',
            })
            self.config.write()

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
