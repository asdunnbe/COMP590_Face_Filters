import tkinter as tk
from PIL import ImageTk, Image

root = tk.Tk() # root is the main window
root.title('Title')

# create select between mouth or eyes
# Labelframe
# Radiobuttons or Labels or List

# create image
img = Image.open('./cam.png')
phimg = ImageTk.PhotoImage(img)
lblimg = tk.Label(image=phimg)

# Scale widget for selecting rotation angle


# submit Button
submitBtn = tk.Button(text='Submit')
# submitBtn = tk.Label(text='submit text')
# submitBtn.bind('<Button-1>', lambda e:open_url('youtube.com'))

# place objects
lblimg.grid(row=0,column=0)
submitBtn.grid(row=1,column=0)

root.mainloop()


# Label parameters
# foreground:   color to draw the text in
# background:   background color of the widget
# padx, pady:   extra padding along the inside border of the widget
# borderwidth:  width of the border around widget
# relief:       border style: flat, raised, sunken, solid, ridge, groove

