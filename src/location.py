#!/usr/bin/python2

import os
from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk
from git import Git
from utils import get_file_path

class NautilusLocation:
    def __init__(self, uri, window):
        self._window = window
        print(uri)
        self._dir = get_file_path(uri)
        self._git = Git(self._dir)

        self._builder = Gtk.Builder()

        self._builder.add_from_file('/usr/share/nautilus-git/data/test.ui')
        self._builder.connect_signals({
            "push_clicked": self._push,
            "pull_clicked": self._pull,
            "fastcommit_clicked": self._fastcommit,
            "atom_clicked": self._open_atom,
            "terminator_clicked": self._open_terminator
        })
        self._build_widgets()

    def _build_widgets(self):
        project_branch = self._git.get_project_branch()
        remote_url = self._git.get_remote_url()
        self._builder.get_object("branch").set_label(project_branch + " - " + remote_url)

    @property
    def main(self):
        return self._builder.get_object("main")

    def _fastcommit(self, *args):
        out = self._git.fast_commit()
        self.messagebox(out)

    def _push(self, *args):
        out = self._git.push()
        self.messagebox(out)

    def _pull(self, *args):
        out = self._git.pull()
        self.messagebox(out)

    def _open_atom(self, *args):
        try:
            os.spawnlp(os.P_NOWAIT, 'atom', 'atom', self._dir)
        except Exception as e:
            self.messagebox(str(e))

    def _open_terminator(self, *args):
        try:
            os.spawnlp(os.P_NOWAIT, 'terminator', 'terminator', '--working-directory=' + self._dir)
        except Exception as e:
            self.messagebox(str(e))

    def messagebox(self, msg):
        self._builder.get_object("message").get_buffer().set_text(msg)
