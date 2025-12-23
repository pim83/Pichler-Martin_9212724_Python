import customtkinter as ctk
from PIL import Image
from style.style import BG_COLOR


class HeaderFrame(ctk.CTkFrame):
    def __init__(self, master, study_vm, on_edit_user=None, height=80):
        super().__init__(master, height=height)

        # always same size
        self.grid_propagate(False)

        self.on_edit_user = on_edit_user

        # left side
        self.title_label = ctk.CTkLabel(
            self,
            text=study_vm.get_study_name(),
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        )
        self.title_label.pack(side="left", padx=20, pady=20)

        # right side
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.pack(side="right", padx=20, pady=15)

        # Name and Matrikelnumber
        self.user_label = ctk.CTkLabel(
            self.right_frame,
            text=study_vm.get_student_name() + "\n" + str(study_vm.get_matrikel_number()),
            justify="right",
            anchor="e",
            font=ctk.CTkFont(size=14)
        )
        self.user_label.pack(side="left", padx=(0, 10))

        # load image
        user_image = ctk.CTkImage(light_image=Image.open("icons/User.png"),
                      dark_image=Image.open("icons/User.png"),
                      size=(35, 35))

        # Options button
        self.options_button = ctk.CTkButton(
            self.right_frame,
            image=user_image,
            text="",
            fg_color="transparent",
            hover_color="gray30",
            width=35,
            height=35,
            corner_radius=25,
            command=self.on_options_click
        )
        self.options_button.pack(side="left")

    def update_user(self, name, matrikel):
        self.user_label.configure(text=f"{name}\n{matrikel}")

    def on_options_click(self):
        if self.on_edit_user:
            self.on_edit_user()