import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk

# root is the main window
root = tk.Tk()
root.title('Title')
root.config(background='#FFF4E0')

COL1 = '#FFF4E0'
COL2 = '#FFBF9B'
COL3 = '#B46060'
COL4 = '#4D4D4D'
SCALE_LENGTH = 200

imgHeight = 300
imgWidth = 300

# styling
s = ttk.Style()
s.theme_use('default')
s.configure('TLabel', background=COL1, foreground=COL4, padding=3)
s.configure('TFrame', background=COL1)
s.configure('TNotebook', background=COL2, borderwidth=0, padding=2)
s.configure('TNotebook.Tab', background=COL2, foreground=COL4, 
            borderwidth=0, padding=3)
s.map('TNotebook.Tab', background=[('selected',COL1), ('focus',COL1)], 
      foreground=[('selected',COL4)])


# create image
imgCvs = tk.Canvas(root, height=imgHeight, width=imgWidth,
                   background=COL1, highlightbackground=COL2)

fW = 2/3 * imgWidth # face width
fH = 1.2*fW # face height
face = imgCvs.create_oval((imgWidth - fW)/2, (imgHeight - fH)/2,
                          (imgWidth + fW)/2, (imgHeight + fH)/2,
                          outline=COL4)

mW = 0.4*fW # mouth width
mH = 0.25*fH # mouthx2 height
mouth = imgCvs.create_arc((imgWidth - mW)/2, (imgHeight + fH/2 - mH)/2,
                          (imgWidth + mW)/2, (imgHeight + fH/2 + mH)/2,
                          outline=COL3, fill=COL3, extent=-180)

eS = int(.32*fW) #eye size (square)

leyeRaw = Image.open('leye.png')
leyeSized = leyeRaw.resize((eS,eS))
leyeImg = ImageTk.PhotoImage(leyeSized)
leye = imgCvs.create_image((imgWidth - fW/2)/2, (imgHeight - fH/6)/2,
                           anchor='center',image=leyeImg)

reyeRaw = Image.open('reye.png')
reyeSized = reyeRaw.resize((eS,eS))
reyeImg = ImageTk.PhotoImage(reyeSized)
reye = imgCvs.create_image((imgWidth + fW/2)/2, (imgHeight - fH/6)/2,
                           anchor='center',image=reyeImg)


# settings, tabs are mouth or eyes
settingsTabs = ttk.Notebook(root)

# eyes tab
eyesTabFrm = ttk.Frame(settingsTabs)

# choose eye rotation angle
eRotationFrm = ttk.Frame(eyesTabFrm)
eRotLbl = ttk.Label(eRotationFrm, text='Rotation')
eRotMinLbl = ttk.Label(eRotationFrm, text='-180°', foreground=COL3)
eRotScl = tk.Scale(eRotationFrm, orient='horizontal',
                  background=COL1,
                  highlightbackground=COL2, troughcolor=COL3,
                  length=SCALE_LENGTH, from_=-180, to=180, showvalue=0,
                  resolution=10)
eRotMaxLbl = ttk.Label(eRotationFrm, text='180°', foreground=COL3)

eRotLbl.grid(row=0, column=1, sticky='W')
eRotMinLbl.grid(row=1, column=0)
eRotScl.grid(row=1, column=1)
eRotMaxLbl.grid(row=1, column=2)

# choose eye resize
eResizeFrm = ttk.Frame(eyesTabFrm)
eResLbl = ttk.Label(eResizeFrm, text='Resize')
eResMinLbl = ttk.Label(eResizeFrm, text='100%', foreground=COL3)
eResScl = tk.Scale(eResizeFrm, orient='horizontal',
                  background=COL1,
                  highlightbackground=COL2, troughcolor=COL3,
                  length=SCALE_LENGTH, from_=1.0, to=5.0, showvalue=0,
                  resolution=0.1) # command= to call function for each change
eResMaxLbl = ttk.Label(eResizeFrm, text='500%', foreground=COL3)

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
mRotMinLbl = ttk.Label(mRotationFrm, text='-180°', foreground=COL3)
mRotScl = tk.Scale(mRotationFrm, orient='horizontal', 
                  background=COL1,
                  highlightbackground=COL2, troughcolor=COL3,
                  length=SCALE_LENGTH, from_=-180, to=180, showvalue=0,
                  resolution=180)
mRotMaxLbl = ttk.Label(mRotationFrm, text='180°', foreground=COL3)

mRotLbl.grid(row=0, column=1, sticky='W')
mRotMinLbl.grid(row=1, column=0)
mRotScl.grid(row=1, column=1)
mRotMaxLbl.grid(row=1, column=2)

# choose mouth resize
mResizeFrm = ttk.Frame(mouthTabFrm)
mResLbl = ttk.Label(mResizeFrm, text='Resize')
mResMinLbl = ttk.Label(mResizeFrm, text='100%', foreground=COL3)
mResScl = tk.Scale(mResizeFrm, orient='horizontal',
                  background=COL1,
                  highlightbackground=COL2, troughcolor=COL3,
                  length=SCALE_LENGTH, from_=1.0, to=5.0, showvalue=0,
                  resolution=0.1)
mResMaxLbl = ttk.Label(mResizeFrm, text='500%', foreground=COL3)

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
                     background=COL3, foreground=COL1,
                     borderwidth=3, relief='flat',
                     padx=5, pady=5)
submitBtn.bind('<Button-1>', lambda e:print('button clicked'))

# place img and settings
imgCvs.grid(row=0, column=0, rowspan=2, 
            sticky='NW', padx=10, pady=10)
settingsTabs.grid(row=0, column=3, columnspan=3, 
                  sticky='N', padx=5, pady=10)
submitBtn.grid(row=1, column=4, 
               sticky='N', padx=3, pady=3)


root.mainloop()
