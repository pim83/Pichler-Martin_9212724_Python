import customtkinter as ctk
from PIL import Image
from style import BG_COLOR, CANVAS_COLOR, TITLE_COLOR
from study import CourseOfStudy, Semester, Module, Assessment


class HeaderFrame(ctk.CTkFrame):
    def __init__(self, master, click, study_data: CourseOfStudy):
        super().__init__(master, height=80, fg_color="transparent", corner_radius=0)
        self.pack_propagate(False)

        self.frame_header_left = ctk.CTkFrame(self, fg_color=CANVAS_COLOR, height=80, corner_radius=0)
        self.frame_header_left.pack(side="left", fill="both", expand=True)

        self.frame_header_right = ctk.CTkFrame(self, fg_color=CANVAS_COLOR, height=80, corner_radius=0)
        self.frame_header_right.pack(side="right", fill="both", expand=True)

        # add a label to the left header frame
        self.label_study_name = ctk.CTkLabel(self.frame_header_left, text=study_data.study_name.upper(), font=("Roboto", 22, "bold"), text_color=TITLE_COLOR, anchor="w")
        self.label_study_name.pack(padx=25, pady=25, fill="both", expand=True)

        # add the menu button
        image = Image.open("menu.png")
        button_image = ctk.CTkImage(light_image=image, dark_image=image, size=(40, 40))
        self.button_image = button_image

        button = ctk.CTkButton(
            master=self.frame_header_right,
            image=self.button_image,
            text="",
            width=40, height=40,
            fg_color="transparent",
            command=click
        )

        button.pack(padx=20, pady=20, side="right")

        # add a label to the left header frame
        self.label_student_name = ctk.CTkLabel(self.frame_header_right, text=study_data.student_name, font=("Roboto", 16, "bold"), text_color=TITLE_COLOR, anchor="e")
        self.label_student_name.pack(side="right")


    def update_labels(self, study_data: CourseOfStudy):
        self.label_study_name.configure(text=study_data.study_name.upper())
        self.label_student_name.configure(text=study_data.student_name)