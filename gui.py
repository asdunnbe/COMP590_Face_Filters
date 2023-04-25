import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk

COL1 = '#FFF4E0'
COL2 = '#FFBF9B'
COL3 = '#B46060'
COL4 = '#4D4D4D'
SCALE_LENGTH = 200

class ImageAlignmentFrame(tk.Tk):
      # COL1 = '#FFF4E0'
      # COL2 = '#FFBF9B'
      # COL3 = '#B46060'
      # COL4 = '#4D4D4D'
      # SCALE_LENGTH = 200

      imgH = 300
      imgW = 300
      
      fW = 2/3 * imgW # face width = 200
      fH = 1.2*fW # face height

      mW = int(0.4*fW) # mouth width = 80
      mH = int(0.15*fH) # mouthx2 height
      mouthRaw = Image.open('assets/mouth.png')
      mouthSized = mouthRaw.resize((mW,mH))
      mouthRotated = mouthSized

      eS = int(.3*fW) # eye size (square) = 64
      leyeRaw = Image.open('assets/leye.png')
      leyeSized = leyeRaw.resize((eS,eS))
      leyeRotated = leyeSized
      
      reyeRaw = Image.open('assets/reye.png')
      reyeSized = reyeRaw.resize((eS,eS))
      reyeRotated = reyeSized

      def __init__(self):
            super(ImageAlignmentFrame, self).__init__()
            self.title('Title')
            self.config(background=COL1)

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
            self.imgCvs = tk.Canvas(self, height=self.imgH, width=self.imgW,
                              background=COL1, highlightbackground=COL2)

            face = self.imgCvs.create_oval((self.imgW - self.fW)/2, (self.imgH - self.fH)/2,
                                    (self.imgW + self.fW)/2, (self.imgH + self.fH)/2,
                                    outline=COL4)

            self.mouthImg = ImageTk.PhotoImage(self.mouthSized)
            self.mouth = self.imgCvs.create_image(self.imgW/2, (self.imgH+self.fH/2)/2,
                                    anchor='center', image=self.mouthImg)

            self.leyeImg = ImageTk.PhotoImage(self.leyeSized)
            self.leye = self.imgCvs.create_image((self.imgW - self.fW/2)/2, (self.imgH - self.fH/6)/2,
                                    anchor='center',image=self.leyeImg)

            self.reyeImg = ImageTk.PhotoImage(self.reyeSized)
            self.reye = self.imgCvs.create_image((self.imgW + self.fW/2)/2, (self.imgH - self.fH/6)/2,
                                    anchor='center',image=self.reyeImg)


            # settings, tabs are mouth or eyes
            settingsTabs = ttk.Notebook(self)

            # eyes tab
            eyesTabFrm = ttk.Frame(settingsTabs)

            # choose eye rotation angle
            eRotationFrm = ttk.Frame(eyesTabFrm)
            eRotLbl = ttk.Label(eRotationFrm, text='Rotation')
            eRotMinLbl = ttk.Label(eRotationFrm, text='-180°', foreground=COL3)
            self.eRotScl = tk.Scale(eRotationFrm, orient='horizontal',
                              background=COL1,
                              highlightbackground=COL2, troughcolor=COL3,
                              length=SCALE_LENGTH, from_=-180, to=180, showvalue=0,
                              resolution=10, command=self.eyeRotate)
            eRotMaxLbl = ttk.Label(eRotationFrm, text='180°', foreground=COL3)

            eRotLbl.grid(row=0, column=1, sticky='W')
            eRotMinLbl.grid(row=1, column=0)
            self.eRotScl.grid(row=1, column=1)
            eRotMaxLbl.grid(row=1, column=2)

            # choose eye resize
            eResizeFrm = ttk.Frame(eyesTabFrm)
            eResLbl = ttk.Label(eResizeFrm, text='Resize')
            eResMinLbl = ttk.Label(eResizeFrm, text='100%', foreground=COL3)
            self.eResScl = tk.Scale(eResizeFrm, orient='horizontal',
                              background=COL1,
                              highlightbackground=COL2, troughcolor=COL3,
                              length=SCALE_LENGTH, from_=1.0, to=2.0, showvalue=0,
                              resolution=0.05, command=self.eyeResize)
            eResMaxLbl = ttk.Label(eResizeFrm, text='200%', foreground=COL3)

            eResLbl.grid(row=0, column=1, sticky='W')
            eResMinLbl.grid(row=1, column=0)
            self.eResScl.grid(row=1, column=1)
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
            self.mRotScl = tk.Scale(mRotationFrm, orient='horizontal', 
                              background=COL1,
                              highlightbackground=COL2, troughcolor=COL3,
                              length=SCALE_LENGTH, from_=-180, to=180, showvalue=0,
                              resolution=180, command=self.mouthRotate)
            mRotMaxLbl = ttk.Label(mRotationFrm, text='180°', foreground=COL3)

            mRotLbl.grid(row=0, column=1, sticky='W')
            mRotMinLbl.grid(row=1, column=0)
            self.mRotScl.grid(row=1, column=1)
            mRotMaxLbl.grid(row=1, column=2)

            # choose mouth resize
            mResizeFrm = ttk.Frame(mouthTabFrm)
            mResLbl = ttk.Label(mResizeFrm, text='Resize')
            mResMinLbl = ttk.Label(mResizeFrm, text='100%', foreground=COL3)
            self.mResScl = tk.Scale(mResizeFrm, orient='horizontal',
                              background=COL1,
                              highlightbackground=COL2, troughcolor=COL3,
                              length=SCALE_LENGTH, from_=1.0, to=2.5, showvalue=0,
                              resolution=0.05, command=self.mouthResize)
            mResMaxLbl = ttk.Label(mResizeFrm, text='250%', foreground=COL3)

            mResLbl.grid(row=0, column=1, sticky='W')
            mResMinLbl.grid(row=1, column=0)
            self.mResScl.grid(row=1, column=1)
            mResMaxLbl.grid(row=1, column=2)


            # place things in mouth tab
            mRotationFrm.pack(pady=10, padx=5)
            mResizeFrm.pack(pady=10, padx=5)
            settingsTabs.add(mouthTabFrm, text='mouth')

            submitBtn = tk.Label(self, text='submit', 
                              background=COL3, foreground=COL1,
                              borderwidth=3, relief='flat',
                              padx=5, pady=5)
            submitBtn.bind('<Button-1>', lambda e:self.getSettings())


            # grid
            self.imgCvs.grid(row=0, column=0, rowspan=2, 
                        sticky='NW', padx=10, pady=10)
            settingsTabs.grid(row=0, column=3, columnspan=3, 
                  sticky='N', padx=5, pady=10)
            submitBtn.grid(row=1, column=4, 
                        sticky='N', padx=3, pady=3)

      def eyeRotate(self, val):
            angle = int(val)

            self.leyeRotated = self.leyeSized.rotate(angle)
            self.leyeImg = ImageTk.PhotoImage(self.leyeRotated)
            self.imgCvs.itemconfig(self.leye, image=self.leyeImg)

            self.reyeRotated = self.reyeSized.rotate(-1* angle)
            self.reyeImg = ImageTk.PhotoImage(self.reyeRotated)
            self.imgCvs.itemconfig(self.reye, image=self.reyeImg)

      def eyeResize(self, val):
            nEyeSize = int( float(val) * self.eS )
            
            self.leyeSized = self.leyeRaw.resize((nEyeSize, nEyeSize))
            self.leyeResized = self.leyeRotated.resize((nEyeSize, nEyeSize))
            self.leyeImg = ImageTk.PhotoImage(self.leyeResized)
            self.imgCvs.itemconfig(self.leye, image=self.leyeImg)
            
            self.reyeSized = self.reyeRaw.resize((nEyeSize, nEyeSize))
            self.reyeResized = self.reyeRotated.resize((nEyeSize, nEyeSize))
            self.reyeImg = ImageTk.PhotoImage(self.reyeResized)
            self.imgCvs.itemconfig(self.reye, image=self.reyeImg)
            # print(f'{eS} * {val} = {nEyeSize}')

      def mouthRotate(self, val):
            angle = int(val)
            self.mouthRotated = self.mouthSized.rotate(angle)
            self.mouthImg = ImageTk.PhotoImage(self.mouthRotated)
            self.imgCvs.itemconfig(self.mouth, image=self.mouthImg)


      def mouthResize(self, val):
            nMouthW = int( float(val) * self.mW )
            nMouthH = int( float(val) * self.mH )
            self.mouthSized = self.mouthRaw.resize((nMouthW, nMouthH))
            self.mouthResized = self.mouthRotated.resize((nMouthW, nMouthH))
            self.mouthImg = ImageTk.PhotoImage(self.mouthResized)
            self.imgCvs.itemconfig(self.mouth, image=self.mouthImg)


      # submit Button
      def getSettings(self):
            print(f'eye rotation: ', self.eRotScl.get())
            print(f'eye resize: ', self.eResScl.get())
            print(f'mouth rotation: ', self.mRotScl.get())
            print(f'mouth resize: ', self.mResScl.get())
            print('button clicked')



if __name__ == '__main__':
      app = ImageAlignmentFrame()
      app.mainloop()
