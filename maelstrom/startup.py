import os
import stat
import subprocess

from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
Builder.load_file("ui/startup.kv")


class Startup(GridLayout):
    def __init__(self, manager, **kwargs):
        self.manager = manager
        self.cwd = os.path.dirname(__file__)
        self.bin_dir = os.path.join(self.cwd, "lightningd/")
        super(Startup, self).__init__(**kwargs)

    def make_executables(self):
        """Make the plugins and the daemons executable

        We make the plugins executable one by one as we must not make a
        non-plugin executable..
        """
        for file in os.listdir(self.bin_dir):
            if "lightningd" in file:
                path = os.path.join(self.bin_dir, file)
                os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)
        for plugin in ["pay", "fundchannel", "autoclean"]:
            path = os.path.join(self.bin_dir, "plugins", plugin)
            os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)

    def start_lightningd(self, proc):
        """Spawns up the lightningd process.

        :param proc: The variable used to store the process informations.
                     We don't want it to be specific to this view.
        """
        self.make_executables()
        lndir = os.path.join(self.cwd, "lightning_dir")
        bin = os.path.join(self.bin_dir, "lightningd")
        # FIXME: Use our custom backend, not sauron + esplora
        api = "https://explorer.bitcoin-lyon.fr/api"
        cmdline = "{} --daemon --lightning-dir {} --sauron-api-endpoint {}"
        cmdline = cmdline.format(bin, lndir, api)
        self.ids.lightningd_output.text = "Running {}\n".format(cmdline)
        proc = subprocess.Popen(cmdline, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        rc = proc.wait(timeout=20)
        # FIXME: Better error handling
        if rc == 0:
            self.manager.show_home()
        else:
            err = "stderr {}\nstdout {}".format(rc,
                                                proc.stderr.read().decode(),
                                                proc.stdout.read().decode())
            self.ids.lightningd_output.text = err
