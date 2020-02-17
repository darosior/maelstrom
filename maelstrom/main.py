import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.base import EventLoop
from kivy import platform
from threading import Thread

from home import Home
from startup import Startup

# kivy.require('2.0.0')


class InterfaceManager(BoxLayout):
    def __init__(self, app, **kwargs):
        self.app = app
        # The views need a reference to their master, e.g. for switching them
        self.home = Home(self)
        self.startup = Startup(self)
        super(InterfaceManager, self).__init__(**kwargs)

    def show_home(self):
        """
        Shows the homepage.
        """
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA,
                                 Permission.CAPTURE_VIDEO_OUTPUT])
        self.clear_widgets()
        self.add_widget(self.home)

    def show_startup(self):
        """
        Shows the startup page, and start lightningd.
        """
        self.clear_widgets()
        self.add_widget(self.startup)


class Csimple(App):
    def __init__(self, **kwargs):
        super(Csimple, self).__init__(**kwargs)
        self.interface_manager = InterfaceManager(self, orientation='vertical')
        self.lightningd_proc = None
        EventLoop.window.bind(on_keyboard=self.key_input)
        self.interface_manager.show_startup()
        # A hack to actually show the startup screen...
        Thread(target=self.interface_manager.startup.start_lightningd,
               args=(self.lightningd_proc,)).start()

    def build(self):
        return self.interface_manager

    def key_input(self, window, key, scancode, codepoint, modifier):
        """
        Overrides the back button (escape on desktop) default behaviour
        """
        if key == 27:
            # If already on the home screen, we close the app
            if hasattr(self.interface_manager.children[0], 'name'):
                if self.interface_manager.children[0].name in {'home',
                                                               'login'}:
                    self.stop()
            # Otherwise we show the home screen (since it is the parent screen
            # of every screens)
            self.interface_manager.show_home()
            return True  # Stop propagation
        return False


if __name__ == '__main__':
    Csimple().run()
