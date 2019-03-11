from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.lang import Builder
from kivy.garden.zbarcam import zbarcam
Builder.load_file('ui/scan.kv')


class Scan(BoxLayout):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        super(Scan, self).__init__(**kwargs)

    def scanned(self):
        """
        A fonction executed when a qrcode is detected.
        """
        # The on_symbols event is also fired when list gets empty, then it would raise an IndexError
        if self.ids.zbarcam.symbols:
            self.manager.show_pay()
            self.manager.pay_widget.show_payment_details(self.ids.zbarcam.symbols[0].data.decode())
