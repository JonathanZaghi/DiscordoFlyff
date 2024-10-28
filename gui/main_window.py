import tkinter as tk
import win32gui
import win32process

from tkinter import ttk
from awakening_bot.background_awake import Worker
from configurations import configurations
from subproces import Utils

class MainWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        neuz = []
        def get_hwnd_from_pid():
            hwnd_list = []
            def callback(hwnd, hwnd_list):
                _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
        
                if window_pid == neuz[int(dropdown.get()[0])][1]:
                    hwnd_list.append(hwnd)

            win32gui.EnumWindows(callback, hwnd_list)
            return hwnd_list[0] if hwnd_list else None
        

        def start_worker():
            hwnd = get_hwnd_from_pid()
            worker = Worker(var.get(), 155, 3, 17, hwnd)

        opcao_selecionada = ""

        try:
            neuz = Utils.get_neuz()
            opcoes = []
            index = 0

            for x in neuz:
                opcoes.append(str(index) + " - " + x[0])
                index = index + 1

            opcao_selecionada = tk.StringVar()
            opcao_selecionada.set("")


            frame = tk.Frame(relief=tk.GROOVE , width=100, height=50, borderwidth=3, padx=8, pady=8)
            frame.place(x=8, y=40)
            
            lbl_select_window = tk.Label(frame,text="Selecione o personagem")
            lbl_select_window.pack(side=tk.TOP, pady=3)

            dropdown = ttk.Combobox(frame, textvariable=opcao_selecionada, values=opcoes, width=40)
            dropdown.pack(side=tk.LEFT, padx=8,)

            def sel():
                print(var.get())

            var = tk.StringVar()

            frame_radios = tk.Frame(width=80, height=50, relief=tk.GROOVE , borderwidth=3, padx=8, pady=8)
            frame_radios.place(x=8, y=113)

            lbl_select_window = tk.Label(frame_radios,text="Selecione os attributos")
            lbl_select_window.grid()
            for index, (key, value) in enumerate(configurations.configuration['attributes'].items()):
                rd = tk.Radiobutton(frame_radios, text=key, variable=var, value=value, command=sel)
                rd.grid(sticky='w')

            frame_value = tk.Frame(width=80, height=50, relief=tk.GROOVE , borderwidth=3, padx=8, pady=8)
            frame_value.place(x=160, y=113, height=269, )

            lbl_value = tk.Label(frame_value,text="Quantidade desejada")
            lbl_value.pack(side=tk.TOP)

            tk.Entry(frame_value).pack()
            
            frm_text = tk.Frame(relief=tk.GROOVE , borderwidth=3, padx=8, pady=8, )
            frm_text.place(x=492, y=40, width=300, height=345)

            tk.Label(frm_text,text="Intervalo de clique: ").grid(row=0)
            ent_interval = tk.Entry(frm_text).grid(row=0, column=1)


            frm_terminal = tk.Frame(relief=tk.GROOVE , borderwidth=3, padx=3, pady=3, bg="#D0D0D0" )
            frm_terminal.place(x=8, y=400, width=782, height=140)

            text_area = tk.Text(frm_terminal, height=10)
            scrollbar = tk.Scrollbar(frm_terminal)
            
            scrollbar.config(command=text_area.yview)
            text_area.config(yscrollcommand=scrollbar.set, width=92,state=tk.DISABLED )

            text_area.pack(side=tk.LEFT)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            tk.Button(text="Começar", padx=5, pady=5, width=20, command=start_worker).place(x=330, y=550)

        except Exception as e:
            print(e)