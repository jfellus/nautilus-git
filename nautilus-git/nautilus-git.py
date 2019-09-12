#!/usr/bin/python2

import sys

from gi import require_version
require_version("Gtk", "3.0")
require_version('Nautilus', '3.0')
from gi.repository import Gtk, Nautilus, GObject

sys.path.insert(0, "/usr/share/nautilus-git/")

from location import NautilusLocation

class NautilusGitLocationWidget(GObject.GObject, Nautilus.LocationWidgetProvider):
    def get_widget(self, uri, window):
        return NautilusLocation(uri, window).main
