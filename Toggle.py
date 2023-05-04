import tkinter as tk

def default():
    pass

class Toggle(tk.Frame):
    """Toggle widget which can toggle between on and off."""
    value = False

    def __init__(self, master, height=25, 
                 background='#ffffff', foreground='#000000',
                 troughcolor='#ff0000', highlightbackground='#0000ff',
                 command=default):
        self.background = background
        self.troughcolor = troughcolor
        self.command = command
        tk.Frame.__init__(self, master, height=height, width=100, background=highlightbackground)

        self.widget = tk.Frame(self, background=background, height=height, width=50, borderwidth=3)

        self.front = tk.Frame(self.widget, background=background, height=height, width=30, relief='raised', borderwidth=2)
        self.back = tk.Label(self.widget, background=background, text='ON', foreground=foreground, width=3)

        self.widget.bind('<Button-1>', lambda e:self.toggle())
        self.front.bind('<Button-1>', lambda e:self.toggle())
        self.back.bind('<Button-1>', lambda e:self.toggle())

        self.front.grid(row=0, column=0)
        self.back.grid(row=0, column=1)
        self.widget.pack(padx=1, pady=1)
        
    def toggle(self):
        if (self.value):
            # turn off
            self.front.grid(row=0, column=0)
            self.value = False
            self.back.config(text='ON', background=self.background)
        else:
            # turn on
            self.front.grid(row=0, column=2)
            self.value = True
            self.back.config(text='', background=self.troughcolor, height=1)
        self.command()

    def getValue(self):
        return self.value
    
if __name__ == '__main__':
    root = tk.Tk()
    toggle = Toggle(root, height=22)
    toggle.pack(padx=20, pady=20)
    root.mainloop()