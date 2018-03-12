#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class ToolboxUI(Gtk.Window):
    _toolbox_ui_id = 0

    def __init__(self):
        Gtk.Window.__init__(self, title="Toolbox")
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.connect("delete-event", self.on_quit)
        self.show_all()

    def on_quit(self, event=None, event2=None):
        Gtk.main_quit()

if __name__ == "__main__":
    print("This module will not function properly if run, please run the core display file instead.")
    win = ToolboxUI()
    Gtk.main()
