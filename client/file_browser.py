import platform
from pathlib import Path
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
Builder.load_file('ui/file_browser.kv')


class FileBrowser(GridLayout):
    def __init__(self, manager, **kwargs):
        super(FileBrowser, self).__init__(**kwargs)
        self.manager = manager

    def system_name(self):
        name = platform.system()
        if name == 'Linux':
            # Whether Android or Linux
            return platform.linux_distribution()[0]
        return name

    def get_path(self):
        system = self.system_name().lower()
        if system == 'android':
            return '/storage/emulated/0'
        else:
            return str(Path.home())

    def select(self, file_list):
        if file_list:
            self.manager.load_cert(file_list[0])
            self.manager.show_login()
