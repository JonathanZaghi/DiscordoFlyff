import tkinter as tk
from tkinter import ttk


from subproces import Utils

class ConfigNeuz(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        def go_back():
            from gui.main_window import MainWindow
            dropdown.destroy()
            label.destroy()
            label2.destroy()
            MainWindow(parent)
        
        def go_back_error():
            from gui.main_window import MainWindow
            label_error.destroy()
            label2.destroy()
            MainWindow(parent)

        try:
            neuz = Utils.get_neuz()
            opcoes = []
            index = 0
            for x in neuz:
                opcoes.append(str(index) + " - " + x[0])
                index = index + 1
            opcao_selecionada = tk.StringVar()
            opcao_selecionada.set("")

            dropdown = ttk.Combobox(parent, textvariable=opcao_selecionada, values=opcoes)
            dropdown.place(x=220, y=260, relwidth=0.5)

            label2 = tk.Button(text="Voltar",
                        font=("Arial Bold", 12),
                        bg="#f0f0f0",
                        command=go_back,
                        fg="black",
                        bd=2,
                        relief="raised",
                        highlightthickness=2,
                        highlightbackground="#e0e0e0")
            label2.place(x=220, y=480,relwidth=0.5, relheight=0.1)

            label = tk.Label(text="Selecione a janela")
            label.place(x=220, y=238,relwidth=0.5)
        except:
            label_error = tk.Label(text="Algo deu errado! Verifique se possui alguma conta logada!")
            label_error.place(x=220, y=240,relwidth=0.5)
            label2 = tk.Button(text="Voltar",
                        font=("Arial Bold", 12),
                        bg="#f0f0f0",
                        command=go_back_error,
                        fg="black",
                        bd=2,
                        relief="raised",
                        highlightthickness=2,
                        highlightbackground="#e0e0e0")
            label2.place(x=220, y=480,relwidth=0.5, relheight=0.1)

        
  

