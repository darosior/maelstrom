import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from home import Home
from login import Login
from file_browser import FileBrowser


class InterfaceManager(BoxLayout):
    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)
        self.file_chooser = FileBrowser()
        self.login = Login(self)
        self.home = Home()

    def show_login(self):
        self.clear_widgets()
        self.add_widget(self.login)

    def show_fb(self):
        self.clear_widgets()
        self.add_widget(self.file_chooser)

class Csimple(App):
    def __init__(self, **kwargs):
        super(Csimple, self).__init__(**kwargs)
        self.interface_manager = InterfaceManager(orientation='vertical')
        self.interface_manager.show_login()
        
    def build(self):
        return self.interface_manager

if __name__ == '__main__':
    Csimple().run()
