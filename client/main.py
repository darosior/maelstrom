import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from home import Home
from login import Login
from file_browser import FileBrowser
from account import Account
import re


class InterfaceManager(BoxLayout):
    def __init__(self, app, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        self.app = app
        self.file_chooser = FileBrowser(self)
        self.login = Login(self)
        self.home = Home()
        # Used to determine which cert to store. Not very elegant but functional
        self.button_pressed = None

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
        else:
            raise

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
            self.login.ids['error'].text = 'Wrong file format for clien key.'
        else:
            # Default port value is 8002
            port = self.login.ids['port'].text if self.login.ids['port'].text else '8002'
            try:
                self.app.account.connect(self.login.ids['ip'].text, int(port))
            except Exception as e:
                if 'Connection refused' in str(e):
                    self.login.ids['error'].text = 'Connection refused at {}:{}.'.format(self.login.ids['ip'].text, port)
                elif 'Invalid argument' in str(e):
                    self.login.ids['error'].text = 'Wrong values for ip and/or port.'
                else:
                    self.login.ids['error'].text = str(e) # ^^


class Csimple(App):
    def __init__(self, **kwargs):
        super(Csimple, self).__init__(**kwargs)
        self.interface_manager = InterfaceManager(self, orientation='vertical')
        self.interface_manager.show_login()
        self.account = Account()

    def build(self):
        return self.interface_manager

if __name__ == '__main__':
    Csimple().run()
