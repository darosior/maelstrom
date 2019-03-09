from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
Builder.load_file('ui/home.kv')


class Home(GridLayout):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        super(Home, self).__init__(**kwargs)

    def update_balance_text(self):
        """
        Formats the balance text with values fetched from the node
        """
        balance_lightning = self.manager.app.account.get_balance('lightning')
        balance_onchain = self.manager.app.account.get_balance('bitcoin')
        self.ids.balance.text = '[b]On chain        : {} sat ({}$)\nOn Lightning : {} sat ({} $)[b]'.format(
            balance_onchain, self.manager.app.to_usd(balance_onchain), balance_lightning,
            self.manager.app.to_usd(balance_lightning))
