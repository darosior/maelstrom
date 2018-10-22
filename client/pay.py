from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
Builder.load_file('ui/pay.kv')


class Pay(GridLayout):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        super(Pay, self).__init__(**kwargs)
        # We hide the confirmation buttons for now
        self.ids.pay.opacity = 0.0
        self.bolt11 = ''
        
    def show_payment_details(self, bolt11):
        """
        Shows the payment details for validation.
        :param invoice: (str) the bolt11 invoice.
        """
        try:
            decoded = self.manager.app.account.decode_invoice(bolt11)
            # Converting the time until expiration to min and msat to sat
            decoded['expiry'] = int(decoded['expiry'])/60
            sat = int(decoded['msatoshi'])/1000
            usd = self.manager.app.to_usd(sat)
            self.ids.payment_details.text = f"Pay {sat} satoshis ({usd}$) to {decoded['payee']} ?\nDescription : {decoded['description']}\nThis invoice expires in {decoded['expiry']}."
            # We keep the valid invoice and activate the confirmation button
            self.bolt11 = bolt11
            self.ids.pay.opacity = 1.0
        except:
            self.ids.payment_details.text = 'Could not decode invoice. Maybe you should try again.'
