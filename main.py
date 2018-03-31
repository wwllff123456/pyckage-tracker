from tkinter import *
import gui
import save
import time
import threading


obj_list = []


def create_main_window():
    root = Tk()
    root.title("Pyckage Tracker")
    root.resizable(1, 0)
    Grid.columnconfigure(root, 0, weight=1)
    # spacer = Frame(root, width=1000)
    # spacer.pack(side=BOTTOM, fill=X)

    setting_list = save.read_save()

    for i in range(len(setting_list)):
        name = setting_list[i][0]
        carrier = setting_list[i][1]
        tracking_number = setting_list[i][2]
        obj_list.append(gui.PackageFrame(root, name, carrier, tracking_number))

    root.mainloop()


class AutoRefresher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def stop(self):
        self._stop().set()

    def run(self):
        time.sleep(5)
        # ============ Auto refresh every __ min ============
        refresh_interval = 15
        while True:
            try:
                time.sleep(refresh_interval*60)
                for item in obj_list:
                    item.refresh_frame()
                    print(item, "refreshed")
            except RuntimeError:
                break
        print("Exit")


refresh = AutoRefresher()
create_main_window()

