import kivy
kivy.require('1.10.1')

from kivy.app import App
from home import Home

class Csimple(App):
    def __init__(self, **kwargs):
        super(Csimple, self).__init__(**kwargs)
        self.home = Home()

    def build(self):
        return self.home


if __name__ == '__main__':
    Csimple().run()