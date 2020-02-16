import os
import subprocess

from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
Builder.load_file("ui/startup.kv")


class Startup(GridLayout):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        super(Startup, self).__init__(**kwargs)

    def start_lightningd(self, proc):
        """Spawns up the lightningd process.

        :param proc: The variable used to store the process informations.
                     We don't want it to be specific to this view.
        """
        cwd = os.path.dirname(__file__)
        bin = os.path.join(cwd, "lightningd/lightningd/lightningd")
        lndir = os.path.join(cwd, "lightning_dir")
        # FIXME: Use our custom backend, not sauron + esplora
        api = "https://explorer.bitcoin-lyon.fr/api"
        cmdline = "{} --daemon --lightning-dir {} --sauron-api-endpoint {}"
        cmdline = cmdline.format(bin, lndir, api)
        self.ids.lightningd_output.text = "Running {}\n".format(cmdline)
        proc = subprocess.Popen(cmdline, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        rc = proc.wait(timeout=20)
        self.ids.lightningd_output.text += "\nExited with {}\n".format(rc)
        # FIXME: Better error handling
        if rc == 0:
            self.manager.show_home()
