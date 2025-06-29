import customtkinter as ctk
from tkinter import ttk
from PIL import Image
from style import BG_COLOR, CANVAS_COLOR, TITLE_COLOR
from study import CourseOfStudy


class SemesterFrame(ctk.CTkFrame):
    def __init__(self, master, frame_left, frame_center, click, study_data: CourseOfStudy):
        super().__init__(master, fg_color="transparent", corner_radius=0)
        self.treeview_semester_map = {}

        for i in range(0, 2):
            for j in range(0, 4):
                target_frame = frame_left if i == 0 else frame_center

                frame = ctk.CTkFrame(target_frame, fg_color=CANVAS_COLOR, corner_radius=20)
                frame.grid(row=j, column=0, sticky="nsew", padx=10, pady=10)
                semester_number = (j + 1) + (i * 4)

                label = ctk.CTkLabel(frame, text=f"SEMESTER {(j+1)+(i*4)}", font=("Roboto", 14, "bold"), text_color=TITLE_COLOR, anchor="w")
                label.grid(padx=15, pady=20, sticky="w")

                frame.grid_rowconfigure(1, weight=1)
                frame.grid_columnconfigure(0, weight=1)

                # create treeview
                style = ttk.Style()
                style.theme_use('clam')
                style.configure("Treeview", background=CANVAS_COLOR, relief="flat", borderwidth=0)
                style.configure("Treeview.Heading", background=CANVAS_COLOR, foreground=TITLE_COLOR, font=("Roboto", 10, "bold"), borderwidth=0)
                style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

                tree = ttk.Treeview(frame, columns=("modul_ID", "module", "ects", "grade"), show="headings", height=4, style="Treeview")
                tree.heading("modul_ID", text="ID", anchor="w")
                tree.heading("module", text="Modul", anchor="w")
                tree.heading("ects", text="Ects", anchor="center")
                tree.heading("grade", text="Note", anchor="center")

                tree.column("modul_ID", width=10, anchor="w")
                tree.column("ects", width=10, anchor="center")
                tree.column("grade", width=10, anchor="center")

                # fill treeview with data
                semester_obj = next((s for s in study_data.semesters if s.semester_number == semester_number), None)

                if semester_obj:
                    for module in semester_obj.modules:
                        grade_str = ""
                        if module.assessment and module.assessment.grade is not None:
                            grade_str = f"{module.assessment.grade:.1f}"

                        if module.module_ID == "":
                            tree.insert("", "end", values=(module.module_ID, module.module_name, "", ""))
                        else:
                            tree.insert("", "end", values=(module.module_ID, module.module_name, str(module.module_ects), grade_str))

                # treeview postion
                tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

                # event binding for the row selection
                tree.bind("<<TreeviewSelect>>", click)

                # add treeview to the map
                self.treeview_semester_map[tree] = semester_number