from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.lang import Builder
from kivy.garden.zbarcam import ZBarCam
Builder.load_file('ui/scan.kv')


class Scan(BoxLayout):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        if platform not in ('linux', 'windows', 'macos'):
            from android.permissions import request_permission, Permission
            request_permission(Permission.CAMERA)
            request_permission(Permission.CAPTURE_VIDEO_OUTPUT)
        super(Scan, self).__init__(**kwargs)

    def scanned(self):
        """
        A fonction executed when a qrcode is detected.
        """
        self.manager.pay_widget.show_payment_details(str(self.ids.zbarcam.symbols()[0].data))
        self.manager.show_pay()
