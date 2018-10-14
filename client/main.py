import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from home import Home
from login import Login
from file_browser import FileBrowser


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
        self.clear_widgets()
        self.add_widget(self.login)

    def show_fb(self, button_pressed):
        self.clear_widgets()
        self.button_pressed = button_pressed
        self.add_widget(self.file_chooser)

    def load_cert(self, filename):
        if self.button_pressed == 'server cert':
            self.app.server_cert = filename
        elif self.button_pressed == 'client cert':
            self.app.client_cert = filename
        elif self.button_pressed == 'client key':
            self.app.client_key = filename
        else:
            raise

class Csimple(App):
    def __init__(self, **kwargs):
        super(Csimple, self).__init__(**kwargs)
        self.interface_manager = InterfaceManager(self, orientation='vertical')
        self.interface_manager.show_login()
        self.server_cert = None
        self.client_cert = None
        self.client_key = None
        
    def build(self):
        return self.interface_manager

if __name__ == '__main__':
    Csimple().run()
