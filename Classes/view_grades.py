import customtkinter as ctk
from PIL import Image
from style import BG_COLOR, CANVAS_COLOR, TITLE_COLOR, COLOR_GOOD, COLOR_BAD
from study import CourseOfStudy, Semester, Module, Assessment
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


def get_all_grades(data):
        grades = []
        for semester in data.semesters:
            for module in semester.modules:
                if module.assessment and module.assessment.grade != 0.0:
                    grades.append(module.assessment.grade)
        return grades


class GradesFrame(ctk.CTkFrame):    
    def __init__(self, master, study_data: CourseOfStudy):
        super().__init__(master, fg_color=CANVAS_COLOR, corner_radius=20)
        
        grades = get_all_grades(study_data)
        if not grades:
            grades = [0]

        x_data = np.array(np.arange(1, len(grades) + 1))
        y_data = np.array(grades)

        average_grade = np.mean(y_data) if len(y_data) > 0 else 0.0
        grade_color = COLOR_GOOD if average_grade < 2.0 else COLOR_BAD


        label_title = ctk.CTkLabel(self, text=f"NOTENDURCHSCHNITT", font=("Roboto", 14, "bold"), text_color=TITLE_COLOR, anchor="w")
        label_title.pack(padx=30, pady=(30,0), anchor="w")

        label_grade = ctk.CTkLabel(self, text=f"{average_grade:.1f}", font=("Roboto", 30, "bold"), text_color=grade_color, anchor="w")
        label_grade.pack(padx=30, pady=(0,0), anchor="w")

        self.fig, ax = plt.subplots(figsize=(3, 2), dpi=75)

        self.fig.patch.set_facecolor(CANVAS_COLOR)
        ax.set_facecolor(CANVAS_COLOR)
        ax.set_xticks(range(1, len(x_data) + 1))

        ax.plot(x_data, y_data, linestyle='-', color='blue')
        ax.set_ylim(5, 1)

        #ax.set_xlabel('Monate')
        ax.set_ylabel('NOTE')
        ax.legend()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True, pady=20)

    
    def close(self):
        plt.close(self.fig)
        if self.canvas:
            self.canvas.get_tk_widget().destroy()