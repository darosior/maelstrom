from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
Builder.load_file('ui/request_payment.kv')
from kivy.garden.qrcode import QRCodeWidget
from kivy.uix.label import Label


class RequestPayment(GridLayout):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        super(RequestPayment, self).__init__(**kwargs)

    def gen_qrcode(self):
        """
        Generates a qrcode containing the invoice for the specified amount in satoshis
        """
        try:
            amount = int(self.ids.amount.text)
        except:
            self.ids.amount.text = ''
            return
        self.ids.qrcode_container.clear_widgets()
        try:
            bolt11 = self.manager.app.account.gen_invoice(amount)['bolt11']
            self.ids.qrcode_container.add_widget(QRCodeWidget(data=bolt11))
        except Exception as e:
            self.ids.qrcode_container.add_widget(Label(text='There was a problem trying to speak to the node.'))
