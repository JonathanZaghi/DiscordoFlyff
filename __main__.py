import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from subproces import Utils


class ConfigWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        def go_back():
            dropdown.destroy()
            label.destroy()
            label2.destroy()
            MainWindow(parent)
        
        def go_back_error():
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

            dropdown = ttk.Combobox(root, textvariable=opcao_selecionada, values=opcoes)
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
            label.place(x=220, y=240,relwidth=0.5)
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




class MainWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        def go_configuration():
            label1.destroy()
            label2.destroy()
            ConfigWindow(parent)
            
            
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

        @staticmethod
        def show():
            label1.place(x=220, y=400,relwidth=0.5, relheight=0.1)
            label2.place(x=220, y=480,relwidth=0.5, relheight=0.1)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Centro especializado em realizar tarefas")
    root.iconphoto(False, tk.PhotoImage(file="resources/images/windows_logo.png"))
    root.resizable(width=False, height=False)

    img = Image.open("resources/images/Screen.png")
    img = img.resize((800, 600))
    photo_img = ImageTk.PhotoImage(img)
    
    background_label = tk.Label(root, image=photo_img)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = photo_img

    MainWindow(root)

    root.mainloop()



