import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from style.style import CANVAS_COLOR, TITLE_COLOR, SIGNAL_COLOR


class GradesFrame(ctk.CTkFrame):
    def __init__(self, master, viewmodel):
        super().__init__(master, fg_color=CANVAS_COLOR, corner_radius=10)

        self.viewmodel = viewmodel

        self.title_label = ctk.CTkLabel(
            self,
            text=f"NOTENDURCHSCHNITT",
            anchor="w",
            justify="left",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TITLE_COLOR
        )
        self.title_label.pack(anchor="w", padx=20, pady=(15, 0))

        self.average_label = ctk.CTkLabel(
            self,
            text=f"{viewmodel.get_grade_average():.1f}",
            anchor="w",
            justify="left",
            font=ctk.CTkFont(size=35, weight="bold"),
            text_color=SIGNAL_COLOR
        )
        self.average_label.pack(anchor="w", padx=20, pady=(0, 10))

        self._create_chart()
        self.refresh()

    def _create_chart(self):
        self.fig = Figure(figsize=(3, 0.6), dpi=100, facecolor=CANVAS_COLOR)
        self.ax = self.fig.add_subplot(111)

        self.ax.set_facecolor(CANVAS_COLOR)
        self.ax.set_ylim(5, 1)
        self.ax.set_yticks([5, 4, 3, 2, 1])
        self.ax.set_ylabel("Note")
        self.ax.get_xaxis().set_visible(False)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def refresh(self):
        grades = self.viewmodel.get_all_grades()

        self.ax.clear()
        self.ax.set_facecolor(CANVAS_COLOR)

        if not grades:
            self.average_label.configure(text="–")
            self.canvas.draw()
            return

        avg = sum(grades) / len(grades)
        self.average_label.configure(text=f"{avg:.1f}")

        x = list(range(1, len(grades) + 1))
        y = grades

        self.ax.plot(x, y, linestyle="-", color=SIGNAL_COLOR, linewidth=2.5)

        self.ax.set_ylim(1, 5)
        self.ax.set_yticks([1, 2, 3, 4, 5])
        self.ax.get_xaxis().set_visible(False)

        self.ax.grid(
            True,
            color="lightgray",
            linestyle="--",
            linewidth=0.5
        )

        for spine in self.ax.spines.values():
            spine.set_color("lightgray")
            spine.set_linewidth(0.5)

        self.ax.tick_params(
            axis="y",
            colors="gray"
        )

        self.canvas.draw()
