#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject, Pango
from multiprocessing import Process, Value, Array
from toolbox import ToolboxUI
from light_settings import LightSettingsUI

class VisualiserUI(Gtk.Window):
    _light_id_counter = 0

    def __init__(self):
        self.ui_running = Value("b", 1)
        Gtk.Window.__init__(self, title="EMPR PC Visualiser")
        self.set_default_size(800, 600)
        self.set_border_width(10)
        self.lights = {}
        self.packet_last_value = Array("B", [0]*512)

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

        self.toolbox_button = button = Gtk.Button(label="Open Toolbox")
        button.connect("clicked", self.on_open_toolbox)
        label.set_mnemonic_widget(button)
        menu_horizontal_box.pack_start(button, False, True, 0)

        button = Gtk.Button(label="Take Single Capture For All")
        button.connect("clicked", self.btn_single_capture)
        label.set_mnemonic_widget(button)
        menu_horizontal_box.pack_start(button, False, True, 0)

        self.cont_cap_button = button = Gtk.Button(label="Start Continuous Capture For All")
        button.connect("clicked", self.btn_multi_capture)
        label.set_mnemonic_widget(button)
        menu_horizontal_box.pack_start(button, False, True, 0)

        self.stop_cont_cap_button = button = Gtk.Button(label="Stop Continuous Capture For All")
        button.connect("clicked", self.btn_stop_multi_capture)
        label.set_mnemonic_widget(button)
        menu_horizontal_box.pack_start(button, False, True, 0)

        button = Gtk.Button(label="About and Help")
        button.connect("clicked", self.btn_help)
        label.set_mnemonic_widget(button)
        menu_horizontal_box.pack_start(button, False, True, 0)

        #Separator
        separator = Gtk.Separator()
        main_vertical_box.pack_start(separator, False, True, 0)

        #Canvas/Stage
        colour = Gdk.color_parse("#222222")
        rgba = Gdk.RGBA.from_color(colour)
        self.stage = stage = Gtk.Layout()
        stage.set_vexpand(True)
        stage.set_hexpand(True)
        stage.override_background_color(0, rgba)

        main_vertical_box.pack_start(stage, True, True, 0)

        self.add(main_vertical_box)

        self.show_all()

        self.stage_width = stage.get_allocation().width
        self.stage_height = stage.get_allocation().height

        self.timeout_id = GObject.timeout_add(75, self.on_timeout, None)

    def add_light(self, name="Light", size=50, xp=50, yp=50, channel_index=1, channel_size=3):
        root = self

        size = size if size > 25 else 25
        print("Adding Light")

        new_light_event = Gtk.EventBox()

        new_light = Gtk.DrawingArea()
        new_light.light_name = name
        new_light.light_size = size
        new_light.light_x = xp
        new_light.light_y = yp
        new_light.light_channel_size = channel_size
        new_light.set_size_request(new_light.light_size,new_light.light_size)
        new_light.light_colour_tuple = (0,0,0)

        def light_draw(self, canvas):
            r,g,b = new_light.light_colour_tuple
            canvas.set_source_rgb(r,g,b)
            canvas.arc(self.light_size//2,self.light_size//2, self.light_size//2, 0, 2*3.141592)
            canvas.fill_preserve()

        new_light.connect('draw', light_draw)
        new_light.light_id = VisualiserUI._light_id_counter
        new_light.light_root = self
        new_light.light_channel_index = channel_index
        self.lights[VisualiserUI._light_id_counter] = new_light
        VisualiserUI._light_id_counter += 1

        new_light_event.add(new_light)
        new_light_event.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)

        def light_click(self, light):
            if new_light not in LightSettingsUI.open_lights:
                LightSettingsUI(root, new_light)

        new_light_event.connect("button_press_event", light_click)

        self.stage.put(new_light_event, (xp/100.0)*(self.stage_width - size), (yp/100.0)*(self.stage_height - size))

        def draw_light():
            self.stage.move(new_light_event, (new_light.light_x/100.0)*(self.stage_width - new_light.light_size), (new_light.light_y/100.0)*(self.stage_height - new_light.light_size))

        new_light.draw_light = draw_light

        new_light_event.show_all()

        self.single_capture_queue = []
        self.multi_capture_queue = []

    def remove_light(self, light):
        del self.lights[light.light_id]
        self.single_capture_queue.remove(light)
        self.multi_capture_queue.remove(light)
        light.destroy()

    def on_open_toolbox(self, button):
        if not ToolboxUI._toolbox_ui_open:
            self.toolbox = ToolboxUI(self)
            self.toolbox_button.set_sensitive(False)

    def on_timeout(self, event=None):
        new_width = self.stage.get_allocation().width
        new_height = self.stage.get_allocation().height
        update = False
        packet = self.packet_last_value[:]
        if new_width != self.stage_width:
            self.stage_width = new_width
            update = True
        if new_height != self.stage_height:
            self.stage_height = new_height
            update = True
        for light in self.lights.values():
            if update:
                light.draw_light()
            if light in self.single_capture_queue or light in self.multi_capture_queue:
                if light.light_channel_index + light.light_channel_size <= 256:
                    if light.light_channel_size == 3:
                        colour_tuple = tuple(packet[light.light_channel_index - 1:light.light_channel_index+2])
                        colour_tuple = (colour_tuple[0] / 255.0, colour_tuple[1] / 255.0, colour_tuple[2] / 255.0)
                        light.light_colour_tuple = colour_tuple
                        light.queue_draw()
                    elif light.light_channel_size == 7 or light.light_channel_size == 8:
                        colour_tuple = tuple(packet[light.light_channel_index:light.light_channel_index+3])
                        colour_tuple = (colour_tuple[0] / 255.0, colour_tuple[1] / 255.0, colour_tuple[2] / 255.0)
                        fade = (packet[light.light_channel_index-1] / 255.0)
                        colour_tuple = (colour_tuple[0] * fade, colour_tuple[1] * fade, colour_tuple[2] * fade)
                        light.light_colour_tuple = colour_tuple
                        light.queue_draw()
                if light in self.single_capture_queue:
                    self.single_capture_queue.remove(light)
        return True

    def btn_single_capture(self, event):
        for light in self.lights.values():
            self.single_capture_queue.append(light)

    def btn_multi_capture(self, button):
        for light in self.lights.values():
            self.multi_capture_queue.append(light)

    def btn_stop_multi_capture(self, button):
        for light in self.lights.values():
            self.multi_capture_queue = []

    def on_quit(self, event=None, event2=None):
        self.ui_running.value = 0
        Gtk.main_quit()

    def on_toolbox_close(self):
        self.toolbox_button.set_sensitive(True)

    @staticmethod
    def create_ui(win):
        win.ui_running.value = 1
        win.connect("delete-event", win.on_quit)
        Gtk.main()

if __name__ == "__main__":
    print("This module will not function properly if run, please run the core display file instead.")
    win = VisualiserUI()
    VisualiserUI.create_ui(win)
