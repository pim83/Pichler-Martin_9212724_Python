import customtkinter as ctk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
from style import BG_COLOR, CANVAS_COLOR, TITLE_COLOR
from view_header import HeaderFrame
from view_semester import SemesterFrame
from view_grades import GradesFrame
from study import CourseOfStudy, Semester, Module, Assessment
from data_handler import save_course_to_file, load_course_from_file, create_empty_course
import tkinter.messagebox as messagebox
from datetime import datetime


class MainWindow(ctk.CTk):
    def __init__(self, study_data: CourseOfStudy = None):
        super().__init__()
        self.title("Studiumsübersicht")
        self.geometry("2000x1200")

        self.study_data = study_data

        # create the header and base frame      
        self.frame_header = ctk.CTkFrame(self)                 
        self.frame_base = ctk.CTkFrame(self)
        
        # create the base frames
        self.frame_base_left = ctk.CTkFrame(self.frame_base)
        self.frame_base_center = ctk.CTkFrame(self.frame_base)
        self.frame_base_right = ctk.CTkFrame(self.frame_base)
        
        # build UI
        self.create_main_frames()

        self.header = HeaderFrame(self.frame_header, self.on_click_account, study_data)
        self.header.pack(fill="both", expand=True)
        
        self.create_base_frames()

        self.semester = SemesterFrame(self.frame_base, self.frame_base_left, self.frame_base_center, self.on_treeview_select, study_data)
        self.treeview_semester_map = self.semester.treeview_semester_map

        self.goal = GradesFrame(self.frame_base_right, study_data)
        self.goal.pack(fill="both", expand=True, padx=10, pady=10)

        self.goal1 = GradesFrame(self.frame_base_right, study_data)
        self.goal1.pack(fill="both", expand=True, padx=10, pady=10)

        self.goal2 = GradesFrame(self.frame_base_right, study_data)
        self.goal2.pack(fill="both", expand=True, padx=10, pady=10)

        


    def create_main_frames(self):
        self.frame_header = ctk.CTkFrame(self, fg_color=CANVAS_COLOR, height=80, corner_radius=0)
        self.frame_header.pack(fill="x")
        self.frame_header.pack_propagate(False)

        self.frame_base = ctk.CTkFrame(self, fg_color=BG_COLOR, height=1120, corner_radius=0)
        self.frame_base.pack(fill="both", expand=True)

        for i in range(3):
            self.frame_base.grid_columnconfigure(i, weight=1)
        self.frame_base.grid_rowconfigure(0, weight=1)


    def on_click_save_account(self):
        self.study_data.study_name = self.study_name_entry.get()
        self.study_data.student_name = self.student_entry.get()
        
        try:
            self.study_data.study_start_date = datetime.strptime(self.start_date_entry.get(), "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Fehler", "Studienstart muss im Format TT.MM.JJJJ sein.")
            
        try:
            self.study_data.module_duration = int(self.duration_entry.get())
        except ValueError:
            self.study_data.module_duration = -1
            messagebox.showerror("Fehler", "Modullaufzeit muss eine Zahl sein.")

        self.header.update_labels(self.study_data)  
        save_course_to_file(self.study_data, "studium.json")
        self.window_account.destroy()


    def on_click_account(self):
        self.window_account = ctk.CTkToplevel(self)
        self.window_account.title("Studieninformationen")
        self.window_account.geometry("400x400")
        self.window_account.grab_set()

        # name
        study_name_label = ctk.CTkLabel(self.window_account, text="Name des Studiums")
        study_name_label.pack(anchor="w", padx=20)
        self.study_name_entry = ctk.CTkEntry(self.window_account)
        self.study_name_entry.pack(pady=5, padx=20, fill="x")
        self.study_name_entry.insert(0, self.study_data.study_name)

        # student name
        student_label = ctk.CTkLabel(self.window_account, text="Name des Studenten")
        student_label.pack(anchor="w", padx=20)
        self.student_entry = ctk.CTkEntry(self.window_account)
        self.student_entry.pack(pady=5, padx=20, fill="x")
        self.student_entry.insert(0, self.study_data.student_name)

        # start date
        start_label = ctk.CTkLabel(self.window_account, text="Start des Studiums (TT.MM.JJJJ)")
        start_label.pack(anchor="w", padx=20)
        self.start_date_entry = ctk.CTkEntry(self.window_account)
        self.start_date_entry.pack(pady=5, padx=20, fill="x")
        self.start_date_entry.insert(0, self.study_data.study_start_date.strftime("%d.%m.%Y"))

        # module duration
        duration_label = ctk.CTkLabel(self.window_account, text="Modullaufzeit (in Monaten)")
        duration_label.pack(anchor="w", padx=20)
        self.duration_entry = ctk.CTkEntry(self.window_account)
        self.duration_entry.pack(pady=5, padx=20, fill="x")
        self.duration_entry.insert(0, str(self.study_data.module_duration))

        save_button = ctk.CTkButton(master=self.window_account, text="Save", command=self.on_click_save_account, corner_radius=50)
        save_button.pack(pady=40, padx=20)       


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
        semester_number = self.treeview_semester_map.get(tree)

        # no selection
        selected_item = tree.focus()
        if not selected_item:
            return

        values = tree.item(selected_item, "values")
        if not values:
            return

        #tree.selection_remove(tree.selection())
        
        # open window
        self.open_window_module(semester_number, selected_item, values)


    def on_click_save_module(self):
        print("Save Module")
        self.window_module.destroy()


    def open_window_module(self, semester_number, selcted_item, values):
        self.window_module = ctk.CTkToplevel(self)
        self.window_module.title("Modul bearbeiten")
        self.window_module.geometry("400x400")
        self.window_module.grab_set()

        # name
        module_ID_label = ctk.CTkLabel(self.window_module, text="Modul ID")
        module_ID_label.pack(anchor="w", padx=20)
        self.module_ID_entry = ctk.CTkEntry(self.window_module)
        self.module_ID_entry.pack(pady=5, padx=20, fill="x")
        self.module_ID_entry.insert(0, values[0])

        # student name
        module_name_label = ctk.CTkLabel(self.window_module, text="Modul Name")
        module_name_label.pack(anchor="w", padx=20)
        self.module_name_entry = ctk.CTkEntry(self.window_module)
        self.module_name_entry.pack(pady=5, padx=20, fill="x")
        self.module_name_entry.insert(0, values[1])

        # start date
        ects_label = ctk.CTkLabel(self.window_module, text="ECTS")
        ects_label.pack(anchor="w", padx=20)
        self.ects_entry = ctk.CTkEntry(self.window_module)
        self.ects_entry.pack(pady=5, padx=20, fill="x")
        self.ects_entry.insert(0, values[2])

        # module duration
        grade_label = ctk.CTkLabel(self.window_module, text="Note")
        grade_label.pack(anchor="w", padx=20)
        self.grade_entry = ctk.CTkEntry(self.window_module)
        self.grade_entry.pack(pady=5, padx=20, fill="x")
        self.grade_entry.insert(0, values[3])

        save_button = ctk.CTkButton(master=self.window_module, text="Save", command=self.on_click_save_module, corner_radius=50)
        save_button.pack(pady=40, padx=20)

        print("Semester_number: ", semester_number)
        print("Selected Item: ", selcted_item)

    
    def close_all_plots(self):
        self.goal.close()
        self.goal1.close()
        self.goal2.close()
