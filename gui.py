from tkinter import *
import webbrowser
import usps
import ups
import save



class PackageFrame:

    def __init__(self, window, package_name, carrier, tracking_number):
        # carrier id: "usps", "ups", "fedex"

        # carrier dictionary, key=carrier name,
        # value tuple:(NAME_displayed, top_bg, main_bg, main_bg_dark, carrier_logo)
        carrier_dict = {"usps": ("USPS", usps.usps_package, "#6faff5", "#e0effc", "#c8e5fc", save.my_path+"usps3.png"),
                        "ups": ("UPS", ups.ups_package, "#fdcb68", "#ffffff", "#ebebe6", save.my_path+"ups.png"),
                        "fedex": ("Fedex",)}

        # ============ Assign values to class variables ============
        self.window = window
        self.package_name = package_name
        self.carrier = carrier.lower()
        self.track_package = carrier_dict[carrier][1]
        self.time_list, self.status_list, self.location_list, self.url = self.track_package(tracking_number)
        self.top_bg = carrier_dict[carrier][2]
        self.main_bg = carrier_dict[carrier][3]
        self.main_bg_dark = carrier_dict[carrier][4]
        self.carrier_logo = PhotoImage(file=carrier_dict[carrier][5])
        self.tracking_number = tracking_number
        self.details_visible = False

        self.create_page()
        self.create_frame()
        self.create_top_bar()
        self.create_detail_frame()
        self.detail_frame.destroy()

    def create_page(self):

        # ============ Create one page for each package. Destroy() on this frame ============
        self.page = Frame(self.window)
        self.page.pack(fill=X, side=TOP)

        # ============ Separation between two pages  ============
        self.separation = Frame(self.page, height=3, bg="gray")
        self.separation.pack(side=BOTTOM, fill=X)

    def create_frame(self):

        # ============ Create main frame for each package. Refresh() on this frame ============
        self.whole_frame = Frame(self.page)
        self.whole_frame.pack(fill=X, side=TOP)

    def create_top_bar(self):

        # ============ Top bar for name, tracking number and current status ============
        self.top_bar = Frame(self.whole_frame, bg=self.top_bg)
        self.top_bar.pack(side=TOP, fill=X)

        # ============ Name frame in top bar for name and tracking number, in left of top bar ============
        self.name_frame = Frame(self.top_bar, bg=self.top_bg)
        self.name_frame.pack(side=LEFT)

        # ============ First line, package name and tracking number ============
        self.name_num_frame = Frame(self.name_frame, bg=self.top_bg)
        self.name_num_frame.pack(fill=X, side=TOP)

        self.name_label = Label(self.name_num_frame, text=str(self.package_name)[:18] + "\t", bg=self.top_bg, font=("arial", "40"))
        self.tracking_number_label = Label(self.name_num_frame, text=self.tracking_number + "\t", bg=self.top_bg, font=("arial", "10"))

        self.est_label = Label(self.name_num_frame, text="Est. ", bg=self.top_bg, font=("arial", "10"))

        self.name_label.grid(row=0, column=0, rowspan=3, sticky=W+S)
        self.tracking_number_label.grid(row=1, column=1, sticky=E+S)
        self.est_label.grid(row=2, column=1, sticky=E+N)

        Grid.columnconfigure(self.name_num_frame, 0, weight=9)
        Grid.columnconfigure(self.name_num_frame, 1, weight=1)



        # ============ Second line, current status ============
        self.current_frame = Frame(self.name_frame, bg=self.top_bg)
        self.current_frame.pack(fill=X, side=BOTTOM)

        self.current_time_label = Label(self.current_frame, text=self.time_list[0]+"\t", bg=self.top_bg, font=("arial", "12"))
        self.current_status_label = Label(self.current_frame, text=str(self.status_list[0]+"                     ")[:25]+"\t", bg=self.top_bg, font=("arial", "12"))
        self.current_location_label = Label(self.current_frame, text=str(self.location_list[0]+"                     ")[:20]+"\t", bg=self.top_bg, font=("arial", "12"))

        self.current_time_label.grid(row=0, column=0, sticky=W)
        self.current_status_label.grid(row=0, column=1, sticky=W)
        self.current_location_label.grid(row=0, column=2, sticky=W)
        # ============ End of name frame ============

        # ============ Buttons, in right of top bar ============
        # ============ Remove entry, most right of top bar ============
        self.remove_icon = PhotoImage(file=save.my_path+"delete.png")
        self.remove_button = Button(self.top_bar, command=self.page.destroy)
        self.remove_button.config(image=self.remove_icon, bg=self.top_bg)
        self.remove_button.pack(side=RIGHT, padx=3, pady=1)

        # ============ Search current location ============
        self.search_icon = PhotoImage(file=save.my_path+"location.png")
        self.search = Button(self.top_bar, command=self.search_map)
        self.search.config(image=self.search_icon, bg=self.top_bg)
        self.search.pack(side=RIGHT, padx=3, pady=3)

        # ============ Refresh status  ============
        self.refresh_icon = PhotoImage(file=save.my_path+"refresh.png")
        self.refresh = Button(self.top_bar, command=self.refresh_frame)
        self.refresh.config(image=self.refresh_icon, bg=self.top_bg)
        self.refresh.pack(side=RIGHT, padx=3, pady=3)
        # ============ Toggle details status  ============

        self.details_icon = PhotoImage(file=save.my_path+"details.png")
        self.details = Button(self.top_bar, command=self.toggle_detail)
        self.details.config(image=self.details_icon, bg=self.top_bg)
        self.details.pack(side=RIGHT, padx=3, pady=3)

        self.web_icon = PhotoImage(file=save.my_path + "web.png")
        self.web = Button(self.top_bar, command=self.goto_website)
        self.web.config(image=self.web_icon, bg=self.top_bg)
        self.web.pack(side=RIGHT, padx=3, pady=3)


        # ============ End of buttons ============

        # ============ Carrier icon  ============
        self.carrier_label = Label(self.top_bar, image=self.carrier_logo, bg=self.top_bg)
        self.carrier_label.pack(side=RIGHT)
        # ============ End of top bar  ============

    def create_detail_frame(self):

        # ============ Detail frame, in the middle, needs to be toggled on/off  ============
        self.detail_frame = Frame(self.whole_frame, bg=self.main_bg)
        self.detail_frame.pack(fill=X)

        # ============ Iterate to create grid for detailed status  ============
        for i in range(1, len(self.time_list)):
            self.label_0 = Label(self.detail_frame, text=self.time_list[i], font=("arial", "9"))
            self.label_1 = Label(self.detail_frame, text=self.status_list[i], font=("arial", "9"))
            self.label_2 = Label(self.detail_frame, text=self.location_list[i], font=("arial", "9"))

            if i % 2 == 0:
                self.label_0.configure(bg=self.main_bg)
                self.label_1.configure(bg=self.main_bg)
                self.label_2.configure(bg=self.main_bg)

            elif i % 2 == 1:
                self.label_0.configure(bg=self.main_bg_dark)
                self.label_1.configure(bg=self.main_bg_dark)
                self.label_2.configure(bg=self.main_bg_dark)

            Grid.columnconfigure(self.detail_frame, 0, weight=2)
            Grid.columnconfigure(self.detail_frame, 1, weight=2)
            Grid.columnconfigure(self.detail_frame, 2, weight=3)
            Grid.rowconfigure(self.detail_frame, 0, weight=1)
            Grid.rowconfigure(self.detail_frame, 1, weight=1)
            Grid.rowconfigure(self.detail_frame, 2, weight=1)


            self.label_0.grid(row=i, column=0, sticky=W + E)
            self.label_1.grid(row=i, column=1, sticky=W + E)
            self.label_2.grid(row=i, column=2, sticky=W + E)

    # ============ Define click buttons command ============
    def search_map(self):
        url = "http://maps.google.com/?q=" + self.location_list[0].replace(" ", ",+")
        webbrowser.open(url)

    def refresh_frame(self):
        self.time_list, self.status_list, self.location_list, self.url = self.track_package(self.tracking_number)
        self.whole_frame.destroy()
        self.create_frame()
        self.create_top_bar()

        if self.details_visible:
            self.create_detail_frame()

    def toggle_detail(self):
        if self.details_visible:
            self.detail_frame.destroy()
            self.details_visible = False
        elif not self.details_visible:
            self.create_detail_frame()
            self.details_visible = True

    def goto_website(self):
        webbrowser.open(self.url)

