from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
Builder.load_file('ui/pay.kv')


class Pay(GridLayout):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        super(Pay, self).__init__(**kwargs)
        # We hide the confirmation buttons for now
        self.ids.pay.opacity = 0.0