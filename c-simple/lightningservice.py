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
        Calls listfunds and returns a dictionnary with two entries :
        'onchain' : a dict of balances onchain by address, and 'onchannel' :
        a dict of all balances onchain by id.
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
        
    def exposed_pay(self):
        """
        
        """
        
