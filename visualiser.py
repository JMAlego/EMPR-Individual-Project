#!/usr/bin/env python3

from GroupCode.monitor_interface import MonitorInterface
from ui import VisualiserUI
from threading import Thread, Semaphore
from multiprocessing import Process, Array, Value

class Visualiser(object):
    def __init__(self):
        self.ui = VisualiserUI()
        self.ui_thread = Process(target=lambda: VisualiserUI.create_ui(self.ui))
        self.monitor = MonitorInterface()
        self.monitor_thread = Thread(target=self.monitor.run)
        self.main_thread = Thread(target=self.main_loop)
        self.running = False

    def run(self):
        self.ui_thread.start()
        self.monitor_thread.start()
        self.running = True
        self.main_thread.start()

    def stop(self, ui=None, event=None):
        self.monitor.stop()
        self.running = False

    def main_loop(self):
        while(self.running):
            if self.ui.ui_running.value == 0:
                self.stop()
                return
            if not self.running:
                return
            if(self.monitor.buffer_semaphore.acquire(True, 2.0)):
                if self.monitor.packets:
                    packet = self.monitor.packets.pop()
                    self.ui.packet_last_value = Array("B", packet)

if __name__ == "__main__":
    vis = Visualiser()
    vis.run()
