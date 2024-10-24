import tkinter as tk

from gui.config_neuz import ConfigNeuz

class MainWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        def go_configuration():
            label1.destroy()
            label2.destroy()
            ConfigNeuz(parent)
            
            
        label1 = tk.Button(width=46, height=2, text="Despertar", relief="raised", padx=16)
        label1.place(x=220, y=400,relwidth=0.5, relheight=0.1)

        label2 = tk.Button(text="Opções",
                           command=go_configuration,
                   font=("Arial Bold", 12),
                   bg="#f0f0f0",
                   fg="black",
                   bd=2,
                   relief="raised",
                   highlightthickness=2,
                   highlightbackground="#e0e0e0")
        
        label2.place(x=220, y=480,relwidth=0.5, relheight=0.1)