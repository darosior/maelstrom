from rpyc import MasterService, Service
from lightning import LightningRpc
import time
import os

class LightningService(Service):
    """
    The service class, used by RPyC to expose methods.
    
    We are intentionnally not exposing all the methods provided by LightningRpc since the wallet doesn't require them.
    This may change in the future if we want to provide a remote access.
    """
    def on_connect(self, conn):
        """
        Executed by RPyC when a connection is set up.

        :param conn: The connection. Kind of a socket
        """
        self.l = LightningRpc(self.get_lightning_daemon())
        
    def on_disconnect(self, conn):
        """
        Executed by RPyC when a connection is close.

        :param conn: The connection. Kind of a socket.
        """
        pass

    # Utility functions

    def get_lightning_daemon(self):
        """
        Getting the daemon to instanciate LightningRpc.
        cf https://github.com/ElementsProject/lightning/blob/master/contrib/pylightning/lightning-pay

        :return: The daemon's location.
        """
        home = os.getenv("HOME")
        if home:
            dir = os.path.join(home, ".lightning")
        else:
            dir = '.'
        return os.path.join(dir, "lightning-rpc")

    def exposed_get_balance(self):
        """
        Calls listfunds and returns a dictionnary with two entries.

        :return: A dictionnary with two keys, 'onchain' : a dict of balances onchain by address, 'onchannel' : a dict of
        all balances on channels by id.
        """
        funds = self.l.listfunds()
        onchain = {}
        onchannel = {}
        for o in funds['outputs']:
            if o['address'] in onchain:
                onchain[o['address']] += int(o['value'])
            else:
                onchain[o['address']] = int(o['value'])
        for c in funds['channels']:
            # It mays be no short id (i.e if funding tx isn't confirmed yet)
            if 'short_channel_id' in c.keys():
                # Unlikely
                if c['short_channel_id'] in onchannel:
                    onchannel[c['short_channel_id']] += int(c['channel_sat'])
                else:
                    onchannel[c['short_channel_id']] = int(c['channel_sat'])
        return dict(onchain = onchain, onchannel = onchannel)
        
    def exposed_pay(self, bolt11, description='', amount=None):
        """
        Call pay in order to pay an invoice, waits while its state is 'pending'.

        This function is highly inspired of https://github.com/ElementsProject/lightning/blob/master/contrib/pylightning/lightning-pay.

        :param bolt11: An encoded payment request
        :param amount: An amount (in msatoshis) to pay, only needed if amount is not in bolt11.
        :return: The status of the payment. Whether 'pending', 'complete', 'failed' (or any lightning-cli error).
        """
        try:
            if self.l.pay(bolt11, amount).get('payment_hash', False):
                return 'complete'
            else:
                return 'failed'
        except:
            return 'failed'
            

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
        payee = decoded_bolt['payee']
        amount = decoded_bolt.get('msatoshi', amount)
        if not amount:
            raise Exception("You have to specify an amount")
        return int(self.l.getroute(payee, amount, 1)['route'][0]['msatoshi']) - int(amount)

    def exposed_gen_invoice(self, msatoshi, label, desc=None):
        """
        Generates an invoice for being paid.
	
        More infos on https://github.com/ElementsProject/lightning/blob/master/doc/lightning-invoice.7.txt
        and https://github.com/ElementsProject/lightning/blob/master/contrib/pylightning/lightning/lightning.py#L149
	   
	:param msatoshi: Payment value in mili satoshis.
	:param label: Unique string or number (treated as a string : '01' != '1')
	:param desc: A description for the payment.
	
	:returns: The invoice (as a list)
	"""
        return self.l.invoice(msatoshi, label, desc)
		
    def exposed_decode_invoice(self, invoice):
        """
        Decodes the specified invoice (as a BOLT11 str).
 	    
        :param invoice: The invoice to decode.
        :return: Decoded invoice, as a dict.
        """
        return self.l.decodepay(invoice)
	
        
