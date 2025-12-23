from tkinter import dialog
import customtkinter as ctk
from view.view_header import HeaderFrame
from view.view_semester import SemesterFrame
from view.view_grades import GradesFrame
from style.style import BG_COLOR
from study_viewmodel import StudyViewModel
from view.view_thesis import ThesisFrame
from view.view_timeline import TimelineFrame


class MainWindow(ctk.CTk):
    def __init__(self, study_viewmodel: StudyViewModel):
        super().__init__()

        # Data
        self.study_viewmodel = study_viewmodel

        # MainWindow
        self.title("Studieninhaltsübersicht")
        self.geometry("2000x1200")

        # Grid mainWindow
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header
        self.header = HeaderFrame(self, study_viewmodel, on_edit_user=self.open_edit_user_dialog,height=80)
        self.header.grid(row=0, column=0, sticky="ew")

       # BaseFrame
        self.base_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        self.base_frame.grid(row=1, column=0, sticky="nsew")

        # BaseFrame Layout
        self.create_base_layout()

        # SemesterFrames
        self.create_semesters(study_viewmodel)

        # GoalFrames
        self.create_goalframes(study_viewmodel)


    def create_base_layout(self):       
        self.base_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.base_frame.grid_rowconfigure(0, weight=1)

        self.frame_left = ctk.CTkFrame(self.base_frame, fg_color="transparent")
        self.frame_center = ctk.CTkFrame(self.base_frame, fg_color="transparent")
        self.frame_right = ctk.CTkFrame(self.base_frame, fg_color="transparent")

        self.frame_left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.frame_center.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame_right.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        for frame in (self.frame_left, self.frame_center):
            frame.grid_columnconfigure(0, weight=1)
            for i in range(4):
                frame.grid_rowconfigure(i, weight=1)


    def create_semesters(self, study_vm):
        # left baseFrame
        for i in range(4):
            sem_frame = SemesterFrame(
                master=self.frame_left,
                semester_number=i+1,
                viewmodel=study_vm,
                click=self.on_tree_click
            )
            sem_frame.grid(row=i, column=0, sticky="nsew", padx=5, pady=5)
    
        # center baseFrame
        for i in range(4,8):
            sem_frame = SemesterFrame(
                master=self.frame_center,
                semester_number=i+1,
                viewmodel=study_vm,
                click=self.on_tree_click
            )
            sem_frame.grid(row=i-4, column=0, sticky="nsew", padx=5, pady=5)

    def create_goalframes(self, study_vm):
        # GradesFrame
        self.grades_frame = GradesFrame(master=self.frame_right, viewmodel=self.study_viewmodel)
        self.grades_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # TimelineFrame
        self.timeline_frame = TimelineFrame(master=self.frame_right, viewmodel=self.study_viewmodel)
        self.timeline_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # ThesisFrame
        self.thesis_frame = ThesisFrame(master=self.frame_right, viewmodel=self.study_viewmodel)
        self.thesis_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        self.frame_right.grid_rowconfigure(0, weight=2)
        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(2, weight=2)
        self.frame_right.grid_columnconfigure(0, weight=1)

    def open_edit_user_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Benutzerdaten ändern")
        dialog.transient(self)      
        dialog.grab_set()           
        dialog.lift()               
        dialog.focus_force()

        name_entry = ctk.CTkEntry(dialog)
        name_entry.insert(0, self.study_viewmodel.get_student_name())
        name_entry.pack(padx=20, pady=10)
        matrikel_entry = ctk.CTkEntry(dialog)
        matrikel_entry.insert(0, str(self.study_viewmodel.get_matrikel_number()))
        matrikel_entry.pack(padx=20, pady=10)

        def save():
            self.study_viewmodel.update_student(
                name_entry.get(),
                int(matrikel_entry.get())
            )
            self.header.update_user(
                name_entry.get(),
                matrikel_entry.get()
            )
            dialog.destroy()

        ctk.CTkButton(dialog, text="Speichern", command=save).pack(pady=10)

    def open_edit_module_dialog(self, tree, item_id, module_id, grade):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Modul bearbeiten")
        dialog.transient(self)
        dialog.grab_set()
        dialog.lift()
        dialog.focus_force()
        ctk.CTkLabel(dialog, text=f"Modul-ID: {module_id}").pack(padx=20, pady=(20, 5))

        grade_entry = ctk.CTkEntry(dialog)
        grade_entry.insert(0, grade)
        grade_entry.pack(padx=20, pady=10)

        def save():
            new_grade = float(grade_entry.get())

            self.study_viewmodel.update_module_grade(
                module_id=module_id,
                new_grade=new_grade
            )

            tree.set(item_id, column="grade", value=new_grade)

            # refresh plot, timeline and thesis frames
            self.grades_frame.refresh()
            self.timeline_frame.refresh()
            self.thesis_frame.refresh()

            dialog.destroy()

        ctk.CTkButton(dialog, text="Speichern", command=save).pack(pady=15)

    def on_tree_click(self, event):
        tree = event.widget
        selected = tree.selection()

        if not selected:
            return

        item_id = selected[0]
        values = tree.item(item_id, "values")

        module_id = values[0] 
        module_name = values[1]
        ects = values[2]
        grade = values[3]

        self.open_edit_module_dialog(
            tree=tree,
            item_id=item_id,
            module_id=module_id,
            grade=grade
        )