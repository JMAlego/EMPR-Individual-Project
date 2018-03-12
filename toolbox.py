#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class ToolboxUI(Gtk.Window):
    _toolbox_ui_open = False
    _new_light_name_count = 1

    def __init__(self):
        Gtk.Window.__init__(self, title="Toolbox")
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.connect("delete-event", self.on_quit)
        self.set_border_width(10)
        self.set_default_size(250, 400)

        main_vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_vertical_box.set_homogeneous(False)

        label = Gtk.Label("Light Toolbox")
        label.set_markup("<b>Light Toolbox</b>")
        main_vertical_box.pack_start(label, False, True, 0)

        new_light_frame = Gtk.Frame(label="New Light")
        new_light_vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        label = Gtk.Label("Name")
        new_light_vertical_box.pack_start(label, False, True, 0)

        entry = Gtk.Entry()
        entry.set_text("Light " + str(ToolboxUI._new_light_name_count))
        new_light_vertical_box.pack_start(entry, False, True, 0)

        label = Gtk.Label("Size")
        new_light_vertical_box.pack_start(label, False, True, 0)

        self.size_adjustment = size_adjustment = Gtk.Adjustment(50, 0, 100, 1, 10, 0)
        scale = Gtk.Scale(adjustment=size_adjustment)
        scale.set_digits(0)
        scale.set_value_pos(Gtk.PositionType.BOTTOM)

        new_light_vertical_box.pack_start(scale, False, True, 0)

        button = Gtk.Button.new_with_label("Add Light")
        button.connect("clicked", self.on_add_light)
        new_light_vertical_box.pack_start(button, False, True, 0)

        padding_box = Gtk.Box(spacing=10)
        padding_box.pack_start(new_light_vertical_box, True, True, 10)
        new_light_frame.add(padding_box)

        main_vertical_box.pack_start(new_light_frame, False, True, 0)

        self.add(main_vertical_box)

        self.show_all()

    def on_add_light(self, button):
        pass

    def on_quit(self, event=None, event2=None):
        Gtk.main_quit()

if __name__ == "__main__":
    print("This module will not function properly if run, please run the core display file instead.")
    win = ToolboxUI()
    Gtk.main()
