import tkinter as tk
from PIL import Image, ImageTk


root = tk.Tk()

root.attributes("-fullscreen", True)
root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
root.update()

canvas_width = root.winfo_width()
canvas_height = root.winfo_height()

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, background="black", highlightthickness=0)
canvas.pack()

img = Image.open("assets/background.png")  # PIL solution
img = img.resize((canvas_width, canvas_height))
img = ImageTk.PhotoImage(img) # convert to PhotoImage
# img = tk.PhotoImage(file="assets/background.png")
canvas.create_image(0, 0, anchor=tk.NW, image=img)

root.mainloop()
