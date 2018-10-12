from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
Builder.load_file('ui/login.kv')

class Login(GridLayout):
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)