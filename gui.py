import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import cv2
from datetime import datetime
import os

from Toggle import Toggle
from Filter import Filter

class ImageAlignmentFrame(tk.Tk):
      COL1 = '#FFF4E0'
      COL2 = '#FFBF9B'
      COL3 = '#B46060'
      COL4 = '#4D4D4D'
      SCALE_LENGTH = 200

      imgH = 300
      imgW = 300
      
      fW = 2/3 * imgW # face width = 200
      fH = 1.2*fW # face height
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
      
      blur = False

      def __init__(self):
            super(ImageAlignmentFrame, self).__init__()
            self.title('Title')
            self.config(background=self.COL1)

            if (not os.path.exists('Screenshots')):
                  os.makedirs('Screenshots')

            # styling
            s = ttk.Style()
            s.theme_use('default')
            s.configure('TLabel', background=self.COL1, foreground=self.COL4, padding=3)
            s.configure('TFrame', background=self.COL1)
            s.configure('TNotebook', background=self.COL2, borderwidth=0, padding=2)
            s.configure('TNotebook.Tab', background=self.COL2, foreground=self.COL4, 
                        borderwidth=0, padding=3)
            s.map('TNotebook.Tab', background=[('selected',self.COL1), ('focus',self.COL1)], 
                  foreground=[('selected',self.COL4)])


            # create image
            self.imgCvs = tk.Canvas(self, height=self.imgH, width=self.imgW,
                              background=self.COL1, highlightbackground=self.COL2)

            face = self.imgCvs.create_oval((self.imgW - self.fW)/2, (self.imgH - self.fH)/2,
                                    (self.imgW + self.fW)/2, (self.imgH + self.fH)/2,
                                    outline=self.COL4)

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
            eRotMinLbl = ttk.Label(eRotationFrm, text='-180°', foreground=self.COL3)
            self.eRotScl = tk.Scale(eRotationFrm, orient='horizontal',
                              background=self.COL1,
                              highlightbackground=self.COL2, troughcolor=self.COL3,
                              length=self.SCALE_LENGTH, from_=-180, to=180, showvalue=0,
                              resolution=5, command=self.eyeRotate)
            eRotMaxLbl = ttk.Label(eRotationFrm, text='180°', foreground=self.COL3)

            eRotLbl.grid(row=0, column=1, sticky='W')
            eRotMinLbl.grid(row=1, column=0)
            self.eRotScl.grid(row=1, column=1)
            eRotMaxLbl.grid(row=1, column=2)

            # choose eye resize
            eResizeFrm = ttk.Frame(eyesTabFrm)
            eResLbl = ttk.Label(eResizeFrm, text='Resize')
            eResMinLbl = ttk.Label(eResizeFrm, text='100%', foreground=self.COL3)
            self.eResScl = tk.Scale(eResizeFrm, orient='horizontal',
                              background=self.COL1,
                              highlightbackground=self.COL2, troughcolor=self.COL3,
                              length=self.SCALE_LENGTH, from_=1, to=2, showvalue=0,
                              resolution=1, command=self.eyeResize)

            eResMaxLbl = ttk.Label(eResizeFrm, text='200%', foreground=self.COL3)

            eResLbl.grid(row=0, column=1, sticky='W')
            eResMinLbl.grid(row=1, column=0)
            self.eResScl.grid(row=1, column=1)
            eResMaxLbl.grid(row=1, column=2)

            # place things in eyes tab
            eRotationFrm.pack(pady=10, padx=5)
            eResizeFrm.pack(pady=10, padx=5)
            settingsTabs.add(eyesTabFrm, text='eyes')

            # other tab
            otherTabFrm = ttk.Frame(settingsTabs)

            # blur background toggle
            blurFrm = ttk.Frame(otherTabFrm)
            self.blurTgl = Toggle(blurFrm, height=22,
                                 background=self.COL1, foreground=self.COL3,
                                 troughcolor=self.COL3, highlightbackground=self.COL2)
            blurLbl = ttk.Label(blurFrm, text='Blur Background')

            self.blurTgl.grid(row=0, column=0, padx=5)
            blurLbl.grid(row=0, column=1, sticky='E')

            # place things in other tab
            blurFrm.pack(pady=10, padx=5)
            settingsTabs.add(otherTabFrm, text='other')


            # submit button
            submitBtn = tk.Label(self, text='submit', 
                              background=self.COL3, foreground=self.COL1,
                              padx=5, pady=5)
            submitBtn.bind('<Button-1>', lambda e:self.openWebCam())

            # grid
            self.imgCvs.grid(row=0, column=1, rowspan=5, 
                        sticky='NW', padx=10, pady=10)
            settingsTabs.grid(row=0, column=2, columnspan=3, 
                        sticky='N', padx=10, pady=10)
            # iconsFrm.grid(row=1, column=2,
            #             sticky='NW', padx=10)
            submitBtn.grid(row=4, column=3,
                        sticky='S', padx=3, pady=10)

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

      def toggleBlur(self):
            print(f'toggle clicked {self.blur}')
            if (self.blur):
                  self.blurTgl.set(1)
                  self.blur = False
            else:
                  self.blurTgl.set(2)
                  self.blur = True

      def openWebCam(self):
            self.getSettings()
            try:
                  self.withdraw()
                  vid = cv2.VideoCapture(0)
                  while(True):
                        ret, frame = vid.read()
                        frame = frame[:,::-1]

                        # face_filter = Filter(use_url=False, input_image=frame)
                        # face_filter.applyEyeFilter(int(self.eResScl.get()), int(self.eRotScl.get()))

                        # new_frame = face_filter.modified_img
                  
                        # display webcam
                        cv2.imshow('press ESC to exit; SPACE to screenshot', frame)

                        k = cv2.waitKey(1)
                        if  k%256 == 27:
                              # ESC pressed
                              break
                        elif k%256 == 32:
                              # SPACE pressed
                              img_name = "Screenshots/{}.png".format(datetime.now().strftime('%Y%m%d%H%M%S'))
                              if (cv2.imwrite(img_name, frame)):
                                    print("{} saved!".format(img_name))

            except:
                  print('webcam failed')
                  tk.messagebox.showerror('Webcam Failure', "Webcam failed")
            finally:
                  # After the loop release the cap object
                  vid.release()
                  # Destroy all the windows
                  cv2.destroyAllWindows()
                  # reopen gui
                  self.deiconify()

      # submit Button
      def getSettings(self):
            try:
                  print(f'eye rotation: ', self.eRotScl.get())
                  print(f'eye resize: ', self.eResScl.get())
                  print(f'blur background: ', self.blur)
            finally:
                  print('button clicked')


if __name__ == '__main__':
      app = ImageAlignmentFrame()
      app.mainloop()
