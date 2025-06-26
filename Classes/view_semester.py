import customtkinter as ctk
from tkinter import ttk
from PIL import Image
from style import BG_COLOR, CANVAS_COLOR, TITLE_COLOR


class SemesterFrame(ctk.CTkFrame):
    def __init__(self, master, frame_left, frame_center, click):
        super().__init__(master, fg_color="transparent", corner_radius=0)

        for i in range(0, 2):
            for j in range(0, 4):
                target_frame = frame_left if i == 0 else frame_center

                frame = ctk.CTkFrame(target_frame, fg_color=CANVAS_COLOR, corner_radius=20)
                frame.grid(row=j, column=0, sticky="nsew", padx=10, pady=10)
                label = ctk.CTkLabel(frame, text=f"SEMESTER {(j+1)+(i*4)}", font=("Roboto", 12, "bold"), text_color=TITLE_COLOR, anchor="w")
                label.grid(padx=20, pady=20, sticky="w")

                frame.grid_rowconfigure(1, weight=1)
                frame.grid_columnconfigure(0, weight=1)

                # create treeview
                style = ttk.Style()
                style.configure("Treeview", background=CANVAS_COLOR, relief="flat", borderwidth=0)
                style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

                tree = ttk.Treeview(frame, columns=("modul_ID", "module", "ects", "grade"), show="headings", height=4, style="Treeview")
                tree.heading("modul_ID", text="ID")
                tree.heading("module", text="Modul")
                tree.heading("ects", text="Ects")
                tree.heading("grade", text="Note")

                tree.column("modul_ID", width=10, anchor="w")
                tree.column("ects", width=10, anchor="center")
                tree.column("grade", width=10, anchor="center")

                # Beispiel-Daten
                tree.insert("", "end", values=("DLBDSEAIS1_D", "Artificial Intelligence", "5", ""))
                tree.insert("", "end", values=("DLBWIRITT", "Einführung in das wissenschaftliche Arbeiten", "5", "2.7"))
                tree.insert("", "end", values=("DLBDSIPWP_D", "Einführung in die Programmierung mit Python", "5", "2.0"))
                tree.insert("", "end", values=("DLBBIMD", "Mathematik: Analysis", "5", ""))
                tree.insert("", "end", values=("DLBKA", "Kollaboratives Arbeiten", "5", "0"))

                # treeview postion
                tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

                # event binding for the row selection
                tree.bind("<<TreeviewSelect>>", click)