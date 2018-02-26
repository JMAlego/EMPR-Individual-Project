#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject, Pango
from multiprocessing import Process, Value, Array

class DisplayUI(Gtk.Window):

    def __init__(self):
        self.ui_running = Value("b", 1)
        Gtk.Window.__init__(self, title="EMPR PC Display")
        self.set_default_size(800, 600)
        self.set_border_width(10)

        #Container Box
        main_vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_vertical_box.set_homogeneous(False)
        #Menu Box
        menu_horizontal_box = Gtk.Box(spacing=10)
        menu_horizontal_box.set_homogeneous(False)
        main_vertical_box.pack_start(menu_horizontal_box, False, True, 0)
        #Menu
        label = Gtk.Label("Menu")
        menu_horizontal_box.pack_start(label, False, True, 0)

        button = Gtk.Button(label="Open Toolbox")
        #button.connect("clicked", self.btn_reset_count)
        label.set_mnemonic_widget(button)
        menu_horizontal_box.pack_start(button, False, True, 0)

        button = Gtk.Button(label="Take Single Capture")
        #button.connect("clicked", self.btn_reset_count)
        label.set_mnemonic_widget(button)
        menu_horizontal_box.pack_start(button, False, True, 0)

        button = Gtk.Button(label="Start Continuous Capture")
        #button.connect("clicked", self.btn_reset_count)
        label.set_mnemonic_widget(button)
        menu_horizontal_box.pack_start(button, False, True, 0)

        button = Gtk.Button(label="Stop Continuous Capture")
        #button.connect("clicked", self.btn_reset_count)
        label.set_mnemonic_widget(button)
        menu_horizontal_box.pack_start(button, False, True, 0)

        #Separator
        separator = Gtk.Separator()
        main_vertical_box.pack_start(separator, False, True, 0)

        #Canvas/Stage
        colour = Gdk.color_parse("#222222")
        rgba = Gdk.RGBA.from_color(colour)
        stage = Gtk.DrawingArea()
        stage.set_size_request(24, 24)
        stage.override_background_color(0, rgba)

        main_vertical_box.pack_start(stage, True, True, 0)

        self.add(main_vertical_box)

        self.timeout_id = GObject.timeout_add(100, self.on_timeout, None)

    def update_data(self, data):
        pass

    def on_timeout(self, event=None):
        return True

    def btn_reset_count(self, event):
        pass

    def btn_single_capture(self, event):
        pass

    def btn_multi_capture(self, event):
        pass

    def btn_create_channel_monitor(self, event):
        pass

    def on_quit(self, event=None, event2=None):
        self.ui_running.value = 0
        Gtk.main_quit()

    @staticmethod
    def create_ui(win):
        win.ui_running.value = 1
        win.connect("delete-event", win.on_quit)
        win.show_all()
        Gtk.main()

if __name__ == "__main__":
    print("This module will not function properly if run, please run the core display file instead.")
    win = DisplayUI()
    DisplayUI.create_ui(win)
