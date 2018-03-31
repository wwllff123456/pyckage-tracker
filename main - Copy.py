from tkinter import *
import gui
import save
import time
import threading


class MainWindow(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.title("Pyckage Tracker")
        self.root.resizable(1, 0)
        Grid.columnconfigure(self.root, 0, weight=1)
        # self.spacer = Frame(self.root, width=1000)
        # self.spacer.pack(side=BOTTOM, fill=X)

        self.obj_list = []

        self.setting_list = save.read_save()

        for i in range(len(self.setting_list)):
            self.name = self.setting_list[i][0]
            self.carrier = self.setting_list[i][1]
            self.tracking_number = self.setting_list[i][2]
            self.obj_list.append(gui.PackageFrame(self.root, self.name, self.carrier, self.tracking_number))

        self.root.mainloop()


a = MainWindow()

# ============ Auto refresh every __ min ============
refresh_interval = 15
while True:
    time.sleep(12)
    for item in a.obj_list:
        item.refresh_frame()
        print(item, "refreshed")


