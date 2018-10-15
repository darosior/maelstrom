from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
Builder.load_file('ui/login.kv')


class Login(GridLayout):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        super(Login, self).__init__(**kwargs)

    def show_fb(self, button_pressed):
        """
        A call to the interface manager, to show the file browser
        :param button_pressed: The button pressed to access the file browser
        """
        self.manager.show_fb(button_pressed)

    def connect(self):
        """
        A call to the interface manager, to setup connection to c-simple server
        """
        self.manager.connect()