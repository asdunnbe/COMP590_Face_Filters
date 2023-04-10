import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk

root = tk.Tk() # root is the main window
root.title('Title')
# root["bg"] = '#FFF4E0'
root.config(background='#FFF4E0')

col1 = '#FFF4E0'
col2 = '#FFBF9B'
col3 = '#B46060'
col4 = '#4D4D4D'

# create image
imgRaw = Image.open('./cam.png')
phimg = ImageTk.PhotoImage(imgRaw)
imgLbl = tk.Label(root, image=phimg, background=col1)

# styling
s = ttk.Style()
s.theme_use('default')
s.configure('TLabel', background=col1, foreground=col4, padding=3)
s.configure('TFrame', background=col1)
s.configure('TNotebook', background=col2, borderwidth=0, padding=2)
s.configure('TNotebook.Tab', background=col2, foreground=col4, 
            borderwidth=0, padding=3)
s.map('TNotebook.Tab', background=[('selected',col1), ('focus',col1)], 
      foreground=[('selected',col4)])

# settings, tabs are mouth or eyes
settingsTabs = ttk.Notebook(root)

# eyes tab
eyesTabFrm = ttk.Frame(settingsTabs)

# choose eye rotation angle
eRotationFrm = ttk.Frame(eyesTabFrm)
eRotLbl = ttk.Label(eRotationFrm, text='Rotation')
eRotMinLbl = ttk.Label(eRotationFrm, text='-180°', foreground=col3)
eRotScl = tk.Scale(eRotationFrm, orient='horizontal', 
                  background=col1,
                  highlightbackground=col2, troughcolor=col3,
                  length=200, from_=-180, to=180, showvalue=0)
eRotMaxLbl = ttk.Label(eRotationFrm, text='180°', foreground=col3)

eRotLbl.grid(row=0, column=1, sticky='W')
eRotMinLbl.grid(row=1, column=0)
eRotScl.grid(row=1, column=1)
eRotMaxLbl.grid(row=1, column=2)

# choose eye resize
eResizeFrm = ttk.Frame(eyesTabFrm)
eResLbl = ttk.Label(eResizeFrm, text='Resize')
eResMinLbl = ttk.Label(eResizeFrm, text='100%', foreground=col3)
eResScl = tk.Scale(eResizeFrm, orient='horizontal',
                  background=col1,
                  highlightbackground=col2, troughcolor=col3,
                  length=200, from_=100, to=500, showvalue=0)
eResMaxLbl = ttk.Label(eResizeFrm, text='500%', foreground=col3)

eResLbl.grid(row=0, column=1, sticky='W')
eResMinLbl.grid(row=1, column=0)
eResScl.grid(row=1, column=1)
eResMaxLbl.grid(row=1, column=2)

# place things in eyes tab
eRotationFrm.pack(pady=10, padx=5)
eResizeFrm.pack(pady=10, padx=5)
settingsTabs.add(eyesTabFrm, text='eyes')


# mouth tab
mouthTabFrm = ttk.Frame(settingsTabs)

# choose mouth rotation angle
mRotationFrm = ttk.Frame(mouthTabFrm)
mRotLbl = ttk.Label(mRotationFrm, text='Rotation')
mRotMinLbl = ttk.Label(mRotationFrm, text='-180°', foreground=col3)
mRotScl = tk.Scale(mRotationFrm, orient='horizontal', 
                  background=col1,
                  highlightbackground=col2, troughcolor=col3,
                  length=200, from_=-180, to=180, showvalue=0)
mRotMaxLbl = ttk.Label(mRotationFrm, text='180°', foreground=col3)

mRotLbl.grid(row=0, column=1, sticky='W')
mRotMinLbl.grid(row=1, column=0)
mRotScl.grid(row=1, column=1)
mRotMaxLbl.grid(row=1, column=2)

# choose mouth resize
mResizeFrm = ttk.Frame(mouthTabFrm)
mResLbl = ttk.Label(mResizeFrm, text='Resize')
mResMinLbl = ttk.Label(mResizeFrm, text='100%', foreground=col3)
mResScl = tk.Scale(mResizeFrm, orient='horizontal',
                  background=col1,
                  highlightbackground=col2, troughcolor=col3,
                  length=200, from_=100, to=500, showvalue=0)
mResMaxLbl = ttk.Label(mResizeFrm, text='500%', foreground=col3)

mResLbl.grid(row=0, column=1, sticky='W')
mResMinLbl.grid(row=1, column=0)
mResScl.grid(row=1, column=1)
mResMaxLbl.grid(row=1, column=2)

# place things in mouth tab
mRotationFrm.pack(pady=10, padx=5)
mResizeFrm.pack(pady=10, padx=5)
settingsTabs.add(mouthTabFrm, text='mouth')

# submit Button
submitBtn = tk.Label(root, text='submit', 
                     background=col3, foreground=col1,
                     borderwidth=3, relief='flat',
                     padx=5, pady=5)
submitBtn.bind('<Button-1>', lambda e:print('button clicked'))

# place img and settings
imgLbl.grid(row=0, column=0, rowspan=2, 
            sticky='NW', padx=3, pady=3)
settingsTabs.grid(row=0, column=3, columnspan=3, 
                  sticky='N', padx=5, pady=5)
submitBtn.grid(row=1, column=4, 
               sticky='N', padx=3, pady=3)


root.mainloop()


# Label parameters
# foreground:   color to draw the text in
# background:   background color of the widget
# padx, pady:   extra padding along the inside border of the widget
# borderwidth:  width of the border around widget
# relief:       border style: flat, raised, sunken, solid, ridge, groove

