import tkinter as tk
from tkinter import ttk
from tkinter.font import Font, nametofont
class Linkbutton(ttk.Button):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Obtener el nombre de la fuente por defecto.
        label_font = nametofont("TkDefaultFont").cget("family")
        self.font = Font(family=label_font, size=9)
        
        # Crear un estilo para el hipervínculo.
        style = ttk.Style()
        style.configure(
            "Link.TLabel", foreground="#357fde", font=self.font)
        
        # Aplicarlo a la clase actual.
        self.configure(style="Link.TLabel", cursor="hand2")
        
        # Configurar los eventos de entrada y salida del mouse.
        self.bind("<Enter>", self.on_mouse_enter)
        self.bind("<Leave>", self.on_mouse_leave)
    
    def on_mouse_enter(self, event):
        # Aplicar subrayado.
        self.font.configure(underline=True)
    
    def on_mouse_leave(self, event):
        # Remover subrayado.
        self.font.configure(underline=False)
class Application(ttk.Frame):
    
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("Hipervínculo en tkinter")
        self.create_widgets()
    
    def create_widgets(self):
        self.link = Linkbutton(self,
            text="Clic en el hipervínculo", command=self.link_clicked)
        self.link.place(x=40, y=70)
        self.place(width=300, height=200)
    
    def link_clicked(self):
        import webbrowser
        webbrowser.open("recursospython.com")
        
main_window = tk.Tk()
app = Application(main_window)
app.mainloop()