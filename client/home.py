from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
Builder.load_file('ui/home.kv')


class Home(GridLayout):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)