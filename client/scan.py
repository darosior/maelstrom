from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.garden.zbarcam import ZBarCam
Builder.load_file('ui/scan.kv')


class Scan(BoxLayout):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        super(Scan, self).__init__(**kwargs)