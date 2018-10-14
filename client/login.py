from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
Builder.load_file('ui/login.kv')


class Login(GridLayout):
    def __init__(self, manager, **kwargs):
        super(Login, self).__init__(**kwargs)
        self.manager = manager
        #self.manager.show_fb()

    def show_fb(self, button_pressed):
        self.manager.show_fb(button_pressed)
