import tkinter as tk

from PIL import Image, ImageTk

from gui.main_window import MainWindow


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



