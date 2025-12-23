from sys import modules
import customtkinter as ctk
from tkinter import ttk
from style.style import CANVAS_COLOR, TITLE_COLOR, TITLE_SIZE


class SemesterFrame(ctk.CTkFrame):
    def __init__(self, master, semester_number, viewmodel, click):
        super().__init__(master, fg_color=CANVAS_COLOR, corner_radius=10, height=200)
        
        self.grid_propagate(False)
        self.viewmodel = viewmodel
        self.semester_number = semester_number
        
        # Label
        label = ctk.CTkLabel(
            self,
            text=f"SEMESTER {semester_number}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TITLE_COLOR,
            anchor="w"
        )
        label.pack(padx=20, pady=(15,30), anchor="w")
        
        # WrapperFrame for Treeview
        tree_frame = ctk.CTkFrame(self, fg_color=CANVAS_COLOR, corner_radius=0)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0,10))

        # Treeview Style
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Treeview",
                        background=CANVAS_COLOR,
                        fieldbackground=CANVAS_COLOR,
                        relief="flat")

        style.configure("Treeview.Heading",
                        background=CANVAS_COLOR,
                        foreground=TITLE_COLOR,
                        font=(None, 10, "bold"),
                        borderwidth=0)

        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        # create Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("modul_ID", "module", "ects", "grade"),
            show="headings",
            height=4,
            style="Treeview"
        )
        self.tree.heading("modul_ID", text="ID", anchor="w")
        self.tree.heading("module", text="Modul", anchor="w")
        self.tree.heading("ects", text="Ects", anchor="center")
        self.tree.heading("grade", text="Note", anchor="center")

        self.tree.column("modul_ID", width=40, anchor="w")
        self.tree.column("module", width=150, anchor="w")
        self.tree.column("ects", width=50, anchor="center")
        self.tree.column("grade", width=50, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", click)

        self.load_data()

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        modules = self.viewmodel.get_modules_for_semester(self.semester_number)

        for module in modules:
            grade = (
                module.assessment.grade
                if module.assessment and module.assessment.grade is not None
                else "-"
            )

            self.tree.insert(
                "",
                "end",
                values=(
                    module.module_ID,
                    module.module_name,
                    module.module_ects,
                    grade
                )
            )