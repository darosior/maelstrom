import kivy
kivy.require('1.10.1')

from kivy.app import App
from home import Home
from login import Login
from file_browser import FileBrowser

class Csimple(App):
    def __init__(self, **kwargs):
        super(Csimple, self).__init__(**kwargs)
        self.login = Login()
        self.file_chooser = FileBrowser()
        self.home = Home()

        
    def build(self):
        return self.login


if __name__ == '__main__':
    Csimple().run()
