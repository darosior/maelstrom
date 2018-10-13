from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
Builder.load_file('ui/file_browser.kv')


class FileBrowser(GridLayout):
    def __init__(self, **kwargs):
        super(FileBrowser, self).__init__(**kwargs)