import customtkinter as ctk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
from style import BG_COLOR, CANVAS_COLOR, TITLE_COLOR
from view_header import HeaderFrame
from view_semester import SemesterFrame


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Studiumsübersicht")
        self.geometry("2000x1200")

        # create the header and base frame
        self.frame_header = ctk.CTkFrame(self)
        self.frame_base = ctk.CTkFrame(self)

        # create the base frames
        self.frame_base_left = ctk.CTkFrame(self.frame_base)
        self.frame_base_center = ctk.CTkFrame(self.frame_base)
        self.frame_base_right = ctk.CTkFrame(self.frame_base)

        # build UI
        self.create_main_frames()

        self.header = HeaderFrame(self.frame_header, self.on_account_click)
        self.header.pack(fill="both", expand=True)
        
        self.create_base_frames()

        self.semester = SemesterFrame(self.frame_header, self.frame_base_left, self.frame_base_center, self.on_treeview_select)
        self.semester.pack(fill="both", expand=True)


    def create_main_frames(self):
        self.frame_header = ctk.CTkFrame(self, fg_color=CANVAS_COLOR, height=80, corner_radius=0)
        self.frame_header.pack(fill="x")
        self.frame_header.pack_propagate(False)

        self.frame_base = ctk.CTkFrame(self, fg_color=BG_COLOR, height=1120, corner_radius=0)
        self.frame_base.pack(fill="both", expand=True)

        for i in range(3):
            self.frame_base.grid_columnconfigure(i, weight=1)
        self.frame_base.grid_rowconfigure(0, weight=1)


    def show_data(self):
        print("Click")


    def on_account_click(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Studieninformationen")
        popup.geometry("400x400")
        popup.grab_set()

        # name
        study_name_label = ctk.CTkLabel(popup, text="Name des Studiums")
        study_name_label.pack(anchor="w", padx=20)
        study_name_entry = ctk.CTkEntry(popup)
        study_name_entry.pack(pady=5, padx=20, fill="x")
        study_name_entry.insert(0, self.header.study_name)

        # student name
        student_label = ctk.CTkLabel(popup, text="Name des Studiums")
        student_label.pack(anchor="w", padx=20)
        student_entry = ctk.CTkEntry(popup)
        student_entry.pack(pady=5, padx=20, fill="x")
        student_entry.insert(0, self.header.student_name)

        # start date
        start_label = ctk.CTkLabel(popup, text="Studienstart (TT.MM.JJJJ)")
        start_label.pack(anchor="w", padx=20)
        start_entry = ctk.CTkEntry(popup)
        start_entry.pack(pady=5, padx=20, fill="x")

        # module duration
        duration_label = ctk.CTkLabel(popup, text="Modulelaufzeit (in Monaten)")
        duration_label.pack(anchor="w", padx=20)
        duration_entry = ctk.CTkEntry(popup)
        duration_entry.pack(pady=5, padx=20, fill="x")

        show_button = ttk.Button(popup, text="Anzeigen", command=self.show_data)
        show_button.grid(row=2, column=0, columnspan=2, pady=10)


    def create_base_frames(self):
        self.frame_base_left = ctk.CTkFrame(self.frame_base, fg_color=BG_COLOR, corner_radius=0)
        self.frame_base_left.grid(row=0, column=0, sticky="nsew", pady=10)
        self.frame_base_left.grid_columnconfigure(0, weight=1)
        for i in range(4):
            self.frame_base_left.grid_rowconfigure(i, weight=1)

        self.frame_base_center = ctk.CTkFrame(self.frame_base, fg_color=BG_COLOR, corner_radius=0)
        self.frame_base_center.grid(row=0, column=1, sticky="nsew", pady=10)
        self.frame_base_center.grid_columnconfigure(0, weight=1)
        for i in range(4):
            self.frame_base_center.grid_rowconfigure(i, weight=1)

        self.frame_base_right = ctk.CTkFrame(self.frame_base, fg_color=BG_COLOR, corner_radius=0)
        self.frame_base_right.grid(row=0, column=2, sticky="nsew", pady=10)
        self.frame_base_right.grid_columnconfigure(0, weight=1)
        for i in range(4):
            self.frame_base_right.grid_rowconfigure(i, weight=1)


    def on_treeview_select(self, event):
        tree = event.widget

        # no selection
        selected_item = tree.focus()
        if not selected_item:
            return

        values = tree.item(selected_item, "values")
        tree.selection_remove(tree.selection())

        # open window
        self.open_module_window(values, tree, selected_item)


    def open_module_window(self, values, tree, item_id):
        popup = ctk.CTkToplevel(self)
        popup.title("Modul bearbeiten")
        popup.geometry("400x300")

        labels = ["Modul-ID", "Modulname", "ECTS", "Note"]
        entries = []

        for i, label_text in enumerate(labels):
            label = ctk.CTkLabel(popup, text=label_text)
            label.pack(pady=(10, 0))
            entry = ctk.CTkEntry(popup)
            entry.insert(0, values[i])
            entry.pack()
            entries.append(entry)