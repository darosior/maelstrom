import platform
from pathlib import Path
from kivy.utils import platform
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
Builder.load_file('ui/file_browser.kv')


class FileBrowser(GridLayout):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        super(FileBrowser, self).__init__(**kwargs)

    def system_name(self):
        name = platform.system()
        if name == 'Linux':
            # Whether Android or Linux
            return platform.linux_distribution()[0]
        return name

    def get_path(self):
        if platform in ['linux', 'macosx', 'windows']:
            return str(Path.home())
        else:
            from android.permissions import request_permission, Permission
            request_permission(Permission.READ_EXTERNAL_STORAGE)
            request_permission(Permission.WRITE_EXTERNAL_STORAGE)
            return '/storage/emulated/0/Download'

    def select(self, file_list):
        if file_list:
            self.manager.load_cert(file_list[0])
            self.manager.show_login()
