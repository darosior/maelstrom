from rpyc import MasterService, Service
from lightning import LightningRpc

class LightningService(Service):
    """
    The service class, used by RPyC to expose methods.
    
    We are intentionnally not exposing all the methods provided by LightningRpc since the wallet doesn't require them.
    This may change in the future if we want to provide a remote access.
    """
    def on_connect(self, conn):
        self.l = LightningRpc('socketfile')
        
    def on_disconnect(self, conn):
        print('\n\n AAAAAAA')
    
    def exposed_get_balance(self):
        """
        Calls listfunds and returns a dictionnary with two entries.

        :return: A dictionnary with two keys, 'onchain' : a dict of balances onchain by address, 'onchannel' : a dict of
        all balances on channels by id.
        """
        funds = self.l.listfunds()
        onchain = {}
        onchannel = {}
        for o in funds['output']:
            if o['address'] in onchain:
                # To test !
                onchain[o['address']] += int(o['value'])
            else:
                onchain[o['address']] = int(o['value'])
        for c in funds['channels']:
            # Unlikely
            if c['short_channel_id'] in onchannel:
                onchannel[c['short_channel_id']] += int(c['channel_sat'])
            else:
                onchannel[c['short_channel_id']] = int(c['channel_sat'])
        return dict(onchain, onchannel)
        
    def exposed_pay(self, bolt11, amount=None):
        """
        Call pay in order to pay an invoice.

        This function is highly inspired of https://github.com/ElementsProject/lightning/blob/master/contrib/pylightning/lightning-pay.

        :param bolt11: An encoded payment request
        :param amount: An amount (in msatoshis) to pay, only needed if amount is not in bolt11.
        :return: The status of the payment. Whether 'pending', 'complete', 'failed' (or any lightning-cli error).
        """
        if bolt11[:2] != 'ln':
            raise Exception('Invoice is malformed')
        decoded_bolt = self.l.decodepay(bolt11)
        amount = decoded_bolt.get('msatoshi', amount)
        if not amount:
            raise Exception("You have to specify an amount")
        payee = decoded_bolt['payee'] # Public key
        hash = decoded_bolt['payment_hash']
        route = self.l.getroute(payee, amount, 1)
        payment_status = self.l.sendpay(route['route'], hash)['status']
        while payment_status == 'pending':
            for p in self.l.listpayments():
                if p['payment_hash'] == hash:
                    payment_status = p['status']
        return payment_status

    def exposed_get_fees(self, bolt11, amount=None):
        """
        Calculate the fees needed to achieve payment.

        :param bolt11: An encoded payment request.
        :param amount: The amount to send.
        :return: The transaction fees (or any lightning-cli error).
        """
        if bolt11[:2] != 'ln':
            raise Exception('Invoice is malformed')
        decoded_bolt = self.l.decodepay(bolt11)
        amount = decoded_bolt.get('msatoshi', amount)
        if not amount:
            raise Exception("You have to specify an amount")
        return self.l.getroute(payee, amount, 1)['route'][0]['msatoshi'] - amount

        
