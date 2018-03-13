#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class ToolboxUI(Gtk.Window):
    _toolbox_ui_open = False
    _new_light_name_count = 1

    def __init__(self, parent):
        Gtk.Window.__init__(self, title="Toolbox")
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.connect("delete-event", self.on_quit)
        self.set_border_width(10)
        self.set_default_size(250, 400)
        ToolboxUI._toolbox_ui_open = True
        self.parent = parent

        main_vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_vertical_box.set_homogeneous(False)

        label = Gtk.Label("Toolbox")
        label.set_markup("<b>Toolbox</b>")
        main_vertical_box.pack_start(label, False, True, 0)

        #New Light Box

        new_light_frame = Gtk.Frame(label="New Light")
        new_light_vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        label = Gtk.Label("Name")
        new_light_vertical_box.pack_start(label, False, True, 0)

        self.light_name = entry = Gtk.Entry()
        entry.set_text("Light " + str(ToolboxUI._new_light_name_count))
        new_light_vertical_box.pack_start(entry, False, True, 0)

        label = Gtk.Label("Channel Index")
        new_light_vertical_box.pack_start(label, False, True, 0)

        self.channel_index = entry = Gtk.Entry()
        entry.connect('changed', lambda self: self.set_text(''.join([i for i in self.get_text().strip() if i in '0123456789'][:3])))
        entry.set_text("1")
        new_light_vertical_box.pack_start(entry, False, True, 0)

        label = Gtk.Label("Size (px)")
        new_light_vertical_box.pack_start(label, False, True, 0)

        self.size_adjustment = size_adjustment = Gtk.Adjustment(50, 25, 250, 1, 10, 0)
        self.scale = scale = Gtk.Scale(adjustment=size_adjustment)
        scale.set_digits(0)
        scale.set_value_pos(Gtk.PositionType.BOTTOM)

        new_light_vertical_box.pack_start(scale, False, True, 0)

        label = Gtk.Label("Channel Size (3, 7, or 8)")
        new_light_vertical_box.pack_start(label, False, True, 0)

        self.channel_size = entry = Gtk.Entry()
        entry.connect('changed', lambda self: self.set_text(''.join([i for i in self.get_text().strip() if i in '378'][:1])))
        entry.set_text("3")
        new_light_vertical_box.pack_start(entry, False, True, 0)

        location_box = Gtk.Box(spacing=10)

        label = Gtk.Label("X%:")
        location_box.pack_start(label, False, True, 0)

        self.x_adjustment = x_adjustment = Gtk.Adjustment(50, 0, 100, 1, 10, 0)
        scale = Gtk.Scale(adjustment=x_adjustment)
        scale.set_digits(0)
        scale.set_value_pos(Gtk.PositionType.BOTTOM)
        location_box.pack_start(scale, True, True, 0)

        label = Gtk.Label("Y%:")
        location_box.pack_start(label, False, True, 0)

        self.y_adjustment = y_adjustment = Gtk.Adjustment(50, 0, 100, 1, 10, 0)
        scale = Gtk.Scale(adjustment=y_adjustment)
        scale.set_digits(0)
        scale.set_value_pos(Gtk.PositionType.BOTTOM)
        location_box.pack_start(scale, True, True, 0)

        new_light_vertical_box.pack_start(location_box, False, True, 0)

        button = Gtk.Button.new_with_label("Add Light")
        button.connect("clicked", self.on_add_light)
        new_light_vertical_box.pack_start(button, False, True, 0)

        padding_box = Gtk.Box(spacing=10)
        padding_box.pack_start(new_light_vertical_box, True, True, 10)
        new_light_frame.add(padding_box)

        main_vertical_box.pack_start(new_light_frame, False, True, 0)

        #End new light box

        #Start Light List

        light_list_frame = Gtk.Frame(label="Light List")
        light_list_vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        padding_box = Gtk.Box(spacing=10)
        padding_box.pack_start(light_list_vertical_box, True, True, 10)
        light_list_frame.add(padding_box)

        main_vertical_box.pack_start(light_list_frame, False, True, 0)

        #End Light List

        self.add(main_vertical_box)

        self.show_all()

    def on_add_light(self, button):
        try:
            channel_index = int(self.channel_index.get_text())
        except:
            channel_index = 1
        if channel_index > 256:
            channel_index = 256
        if channel_index < 1:
            channel_index = 1
        try:
            channel_size = int(self.channel_size.get_text())
        except:
            channel_size = 3
        self.parent.add_light(self.light_name.get_text(), self.size_adjustment.get_value(), self.x_adjustment.get_value(), self.y_adjustment.get_value(), channel_index, channel_size)
        ToolboxUI._new_light_name_count += 1
        self.light_name.set_text("Light " + str(ToolboxUI._new_light_name_count))

    def on_quit(self, event=None, event2=None):
        self.parent.on_toolbox_close()
        ToolboxUI._toolbox_ui_open = False
        self.destroy()

if __name__ == "__main__":
    print("This module will not function properly if run, please run the core display file instead.")
    win = ToolboxUI(None)
    Gtk.main()
