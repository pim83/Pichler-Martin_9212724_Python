import customtkinter as ctk
from PIL import Image
from style import BG_COLOR, CANVAS_COLOR, TITLE_COLOR


class HeaderFrame(ctk.CTkFrame):
    def __init__(self, master, click):
        super().__init__(master, height=80, fg_color="transparent", corner_radius=0)
        self.pack_propagate(False)

        self.frame_header_left = ctk.CTkFrame(self, fg_color=CANVAS_COLOR, height=80, corner_radius=0)
        self.frame_header_left.pack(side="left", fill="both", expand=True)

        self.frame_header_right = ctk.CTkFrame(self, fg_color=CANVAS_COLOR, height=80, corner_radius=0)
        self.frame_header_right.pack(side="right", fill="both", expand=True)

        # add a label to the left header frame
        label_title = ctk.CTkLabel(self.frame_header_left, text="B.SC. ANGEWANDTE KÜNSTLICHE INTELLIGENZ", font=("Roboto", 22, "bold"), text_color=TITLE_COLOR, anchor="w")
        label_title.pack(padx=25, pady=25, fill="both", expand=True)

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
        label_name = ctk.CTkLabel(self.frame_header_right, text="Martin Pichler", font=("Roboto", 16, "bold"), text_color=TITLE_COLOR, anchor="e")
        label_name.pack(side="right")

