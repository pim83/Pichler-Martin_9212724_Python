import customtkinter as ctk
from style.style import CANVAS_COLOR, TITLE_COLOR, BAR_BG_COLOR, SIGNAL_COLOR


class ThesisFrame(ctk.CTkFrame):
    def __init__(self, master, viewmodel):
        super().__init__(master, fg_color=CANVAS_COLOR, corner_radius=10)

        self.viewmodel = viewmodel

        # Titel1
        self.title1_label = ctk.CTkLabel(
            self,
            text=f"BENÖTIGTE ECTS FÜR DIE THESIS",
            anchor="w",
            justify="left",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TITLE_COLOR
        )
        self.title1_label.pack(anchor="w", padx=20, pady=(15, 0))

        # progress in ects
        self.progress_label = ctk.CTkLabel(
            self,
            text=f"{viewmodel.get_ects_progress_string()}",
            anchor="w",
            justify="left",
            font=ctk.CTkFont(size=35, weight="bold"),
            text_color=SIGNAL_COLOR
        )
        self.progress_label.pack(anchor="w", padx=20, pady=(0, 10))

        # Container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=(0, 20))

        # Progressbar
        self.progress_bar = ctk.CTkProgressBar(
            container,
            fg_color=BAR_BG_COLOR,
            progress_color=SIGNAL_COLOR,
            corner_radius=5
        )
        self.progress_bar.set(viewmodel.get_study_progress())
        self.progress_bar.pack(fill="x", pady=(0, 20))

        # Titel2
        title2_label = ctk.CTkLabel(
            self,
            text=f"BERECHNETER BEGINN DER THESIS",
            anchor="w",
            justify="left",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TITLE_COLOR
        )
        title2_label.pack(anchor="w", padx=20, pady=(0, 0))

        # tesisstart date
        self.tesisstart_label = ctk.CTkLabel(
            self,
            text=f"{viewmodel.get_thesis_start_date()}",
            anchor="w",
            justify="left",
            font=ctk.CTkFont(size=35, weight="bold"),
            text_color=SIGNAL_COLOR
        )
        self.tesisstart_label.pack(anchor="w", padx=20, pady=(0, 0))

    def refresh(self):       
        self.progress_label.configure(text=self.viewmodel.get_ects_progress_string())
        self.progress_bar.set(self.viewmodel.get_study_progress())
        self.tesisstart_label.configure(text=str(self.viewmodel.get_thesis_start_date()))
        