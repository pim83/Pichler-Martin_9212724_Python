import customtkinter as ctk
from style.style import CANVAS_COLOR, TITLE_COLOR, BAR_BG_COLOR, SIGNAL_COLOR


class TimelineFrame(ctk.CTkFrame):
    def __init__(self, master, viewmodel):
        super().__init__(master, fg_color=CANVAS_COLOR, corner_radius=10)

        self.viewmodel = viewmodel
        
        # Titel1
        self.title1_label = ctk.CTkLabel(
            self,
            text=f"FORTSCHRITT DES STUDIUMS",
            anchor="w",
            justify="left",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TITLE_COLOR
        )
        self.title1_label.pack(anchor="w", padx=20, pady=(15, 0))

        # progress in %
        self.progress_label = ctk.CTkLabel(
            self,
            text=f"{int(viewmodel.get_study_progress() * 100)}%",
            anchor="w",
            justify="left",
            font=ctk.CTkFont(size=35, weight="bold"),
            text_color=SIGNAL_COLOR
        )
        self.progress_label.pack(anchor="w", padx=20, pady=(0, 10))

        # Container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", expand=False, padx=20, pady=(0, 20))

        # Progressbar
        self.progress_bar = ctk.CTkProgressBar(
            container,
            fg_color=BAR_BG_COLOR,
            progress_color=SIGNAL_COLOR,
            corner_radius=5
        )
        self.progress_bar.set(viewmodel.get_study_progress())
        self.progress_bar.pack(fill="x", expand=False, pady=(0, 20))

        self.title2_label = ctk.CTkLabel(
            container,
            text=f"ABGESCHLOSSENE MODULE",
            anchor="w",
            justify="left",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TITLE_COLOR
        )
        self.title2_label.pack(anchor="w", pady=(10, 0))

        self.modules_label = ctk.CTkLabel(
            container,
            text=f"{viewmodel.get_module_progress_text()}",
            anchor="w",
            justify="left",
            font=ctk.CTkFont(size=35, weight="bold"),
            text_color=SIGNAL_COLOR
        )
        self.modules_label.pack(anchor="w", pady=(0, 25))
       
        self.title3_label = ctk.CTkLabel(
            container,
            text=f"BERECHNETES ABSCHLUSSDATUM",
            anchor="w",
            justify="left",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TITLE_COLOR
        )
        self.title3_label.pack(anchor="w", pady=(0, 0))

        self.enddate_label = ctk.CTkLabel(
            container,
            text=f"{str(viewmodel.get_estimated_end_date())}",
            anchor="w",
            justify="left",
            font=ctk.CTkFont(size=35, weight="bold"),
            text_color=SIGNAL_COLOR
        )
        self.enddate_label.pack(anchor="w", pady=(0, 0))


    def refresh(self):           
        progress = self.viewmodel.get_study_progress()
        self.progress_label.configure(text=f"{int(progress * 100)}%")
        self.progress_bar.set(progress)

        self.modules_label.configure(text=self.viewmodel.get_module_progress_text())
        self.enddate_label.configure(text=str(self.viewmodel.get_estimated_end_date()))
        