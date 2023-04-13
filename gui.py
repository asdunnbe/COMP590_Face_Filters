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

fW = 2/3 * imgWidth # face width = 200
fH = 1.2*fW # face height
face = imgCvs.create_oval((imgWidth - fW)/2, (imgHeight - fH)/2,
                          (imgWidth + fW)/2, (imgHeight + fH)/2,
                          outline=COL4)

mW = int(0.4*fW) # mouth width = 80
mH = int(0.15*fH) # mouthx2 height
mouthRaw = Image.open('mouth.png')
mouthSized = mouthRaw.resize((mW,mH))
mouthImg = ImageTk.PhotoImage(mouthSized)
mouth = imgCvs.create_image(imgWidth/2, (imgHeight+fH/2)/2,
                            anchor='center', image=mouthImg)

eS = int(.3*fW) # eye size (square) = 64

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
def eyeResize(val):
      nEyeSize = int( float(val) * eS )
      global leyeImg
      leyeSized = leyeRaw.resize((nEyeSize, nEyeSize))
      leyeImg = ImageTk.PhotoImage(leyeSized)
      imgCvs.itemconfig(leye, image=leyeImg)
      global reyeImg
      reyeSized = reyeRaw.resize((nEyeSize, nEyeSize))
      reyeImg = ImageTk.PhotoImage(reyeSized)
      imgCvs.itemconfig(reye, image=reyeImg)
      # print(f'{eS} * {val} = {nEyeSize}')


eResizeFrm = ttk.Frame(eyesTabFrm)
eResLbl = ttk.Label(eResizeFrm, text='Resize')
eResMinLbl = ttk.Label(eResizeFrm, text='100%', foreground=COL3)
eResScl = tk.Scale(eResizeFrm, orient='horizontal',
                  background=COL1,
                  highlightbackground=COL2, troughcolor=COL3,
                  length=SCALE_LENGTH, from_=1.0, to=2.0, showvalue=0,
                  resolution=0.05, command=eyeResize)
eResMaxLbl = ttk.Label(eResizeFrm, text='200%', foreground=COL3)

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
def mouthResize(val):
      nMouthW = int( float(val) * mW )
      nMouthH = int( float(val) * mH )
      global mouthImg
      mouthSized = mouthRaw.resize((nMouthW, nMouthH))
      mouthImg = ImageTk.PhotoImage(mouthSized)
      imgCvs.itemconfig(mouth, image=mouthImg)

mResizeFrm = ttk.Frame(mouthTabFrm)
mResLbl = ttk.Label(mResizeFrm, text='Resize')
mResMinLbl = ttk.Label(mResizeFrm, text='100%', foreground=COL3)
mResScl = tk.Scale(mResizeFrm, orient='horizontal',
                  background=COL1,
                  highlightbackground=COL2, troughcolor=COL3,
                  length=SCALE_LENGTH, from_=1.0, to=2.5, showvalue=0,
                  resolution=0.05, command=mouthResize)
mResMaxLbl = ttk.Label(mResizeFrm, text='250%', foreground=COL3)

mResLbl.grid(row=0, column=1, sticky='W')
mResMinLbl.grid(row=1, column=0)
mResScl.grid(row=1, column=1)
mResMaxLbl.grid(row=1, column=2)

# place things in mouth tab
mRotationFrm.pack(pady=10, padx=5)
mResizeFrm.pack(pady=10, padx=5)
settingsTabs.add(mouthTabFrm, text='mouth')

# submit Button
def getSettings():
    print(f'eye rotation: ', eRotScl.get())
    print(f'eye resize: ', eResScl.get())
    print(f'mouth rotation: ', mRotScl.get())
    print(f'mouth resize: ', mResScl.get())
    print('button clicked')

submitBtn = tk.Label(root, text='submit', 
                     background=COL3, foreground=COL1,
                     borderwidth=3, relief='flat',
                     padx=5, pady=5)
submitBtn.bind('<Button-1>', lambda e:getSettings())

# place img and settings
imgCvs.grid(row=0, column=0, rowspan=2, 
            sticky='NW', padx=10, pady=10)
settingsTabs.grid(row=0, column=3, columnspan=3, 
                  sticky='N', padx=5, pady=10)
submitBtn.grid(row=1, column=4, 
               sticky='N', padx=3, pady=3)

root.mainloop()
