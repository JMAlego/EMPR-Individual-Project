#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class LightSettingsUI(Gtk.Window):
    open_lights = []

    def __init__(self, parent, light):
        Gtk.Window.__init__(self, title="Light Settings")
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.connect("delete-event", self.on_quit)
        self.set_border_width(10)
        self.set_default_size(250, 250)
        self.parent = parent
        self.light = light
        self.complete = False

        LightSettingsUI.open_lights.append(light)

        main_vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_vertical_box.set_homogeneous(False)

        label = Gtk.Label("Light Settings")
        label.set_markup("<b>Light Settings</b>")
        main_vertical_box.pack_start(label, False, True, 0)

        #New Light Box

        new_light_vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        label = Gtk.Label("Name")
        new_light_vertical_box.pack_start(label, False, True, 0)

        self.light_name = entry = Gtk.Entry()
        entry.set_text(light.light_name)
        entry.connect('changed', self.on_update)
        new_light_vertical_box.pack_start(entry, False, True, 0)

        label = Gtk.Label("Channel Index")
        new_light_vertical_box.pack_start(label, False, True, 0)

        self.channel_index = entry = Gtk.Entry()
        entry.connect('changed', self.on_update)
        entry.set_text(str(light.light_channel_index))
        new_light_vertical_box.pack_start(entry, False, True, 0)

        label = Gtk.Label("Size (px)")
        new_light_vertical_box.pack_start(label, False, True, 0)

        self.size_adjustment = size_adjustment = Gtk.Adjustment(50, 25, 250, 1, 10, 0)
        size_adjustment.connect('value-changed', self.on_update)
        self.scale = scale = Gtk.Scale(adjustment=size_adjustment)
        scale.set_digits(0)
        scale.set_value(light.light_size)
        scale.set_value_pos(Gtk.PositionType.BOTTOM)

        new_light_vertical_box.pack_start(scale, False, True, 0)

        label = Gtk.Label("Channel Size (3, 7, or 8)")
        new_light_vertical_box.pack_start(label, False, True, 0)

        self.channel_size = entry = Gtk.Entry()
        entry.connect('changed', self.on_update)
        entry.set_text("3")
        entry.root = self
        new_light_vertical_box.pack_start(entry, False, True, 0)

        location_box = Gtk.Box(spacing=10)

        label = Gtk.Label("X%:")
        location_box.pack_start(label, False, True, 0)

        self.x_adjustment = x_adjustment = Gtk.Adjustment(50, 0, 100, 1, 10, 0)
        x_adjustment.connect('value-changed', self.on_update)
        scale = Gtk.Scale(adjustment=x_adjustment)
        scale.set_digits(0)
        scale.set_value(light.light_x)
        scale.set_value_pos(Gtk.PositionType.BOTTOM)
        location_box.pack_start(scale, True, True, 0)

        label = Gtk.Label("Y%:")
        location_box.pack_start(label, False, True, 0)

        self.y_adjustment = y_adjustment = Gtk.Adjustment(50, 0, 100, 1, 10, 0)
        y_adjustment.connect('value-changed', self.on_update)
        scale = Gtk.Scale(adjustment=y_adjustment)
        scale.set_digits(0)
        scale.set_value(light.light_y)
        scale.set_value_pos(Gtk.PositionType.BOTTOM)
        location_box.pack_start(scale, True, True, 0)

        new_light_vertical_box.pack_start(location_box, False, True, 0)

        button = Gtk.Button.new_with_label("Remove Light")
        button.connect("clicked", self.on_remove_light)
        new_light_vertical_box.pack_start(button, False, True, 0)

        button = Gtk.Button.new_with_label("Single Capture Light")
        button.connect("clicked", self.on_update_light)
        new_light_vertical_box.pack_start(button, False, True, 0)

        self.cont_cap_btn = button = Gtk.Button.new_with_label("Enable Continuous Capture")
        button.connect("clicked", self.on_cont_light)
        if light in self.parent.multi_capture_queue:
            button.set_sensitive(False)
        new_light_vertical_box.pack_start(button, False, True, 0)

        self.dis_cont_cap_btn = button = Gtk.Button.new_with_label("Disable Continuous Capture")
        button.connect("clicked", self.on_dis_cont_light)
        if light not in self.parent.multi_capture_queue:
            button.set_sensitive(False)
        new_light_vertical_box.pack_start(button, False, True, 0)

        main_vertical_box.pack_start(new_light_vertical_box, False, True, 0)

        self.add(main_vertical_box)

        self.show_all()

        self.complete = True

    def on_update_light(self, event=None):
        self.parent.single_capture_queue.append(self.light)

    def on_cont_light(self, event=None):
        self.dis_cont_cap_btn.set_sensitive(True)
        self.cont_cap_btn.set_sensitive(False)
        self.parent.multi_capture_queue.append(self.light)

    def on_dis_cont_light(self, event=None):
        self.dis_cont_cap_btn.set_sensitive(False)
        self.cont_cap_btn.set_sensitive(True)
        self.parent.multi_capture_queue.remove(self.light)

    def on_remove_light(self, event=None):
        self.parent.remove_light(self.light)
        self.on_quit()

    def on_quit(self, event=None, event2=None):
        LightSettingsUI.open_lights.remove(self.light)
        self.destroy()

    def on_update(self, event=None):
        if self.complete:
            self.channel_size.set_text(''.join([i for i in self.channel_size.get_text().strip() if i in '378'][:1]))
            self.channel_index.set_text(''.join([i for i in self.channel_index.get_text().strip() if i in '0123456789'][:3]))
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
            self.light.light_name = self.light_name.get_text()
            self.light.light_channel_size = channel_size
            self.light.light_channel_index = channel_index
            self.light.light_x = self.x_adjustment.get_value()
            self.light.light_y = self.y_adjustment.get_value()
            self.light.light_size = self.size_adjustment.get_value()
            self.light.draw_light()
            self.light.set_size_request(self.light.light_size,self.light.light_size)
            self.light.queue_draw()

if __name__ == "__main__":
    print("This module will not function properly if run, please run the core display file instead.")
    win = ToolboxUI(None)
    Gtk.main()
