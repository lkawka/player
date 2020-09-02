import tkinter as tk
from datetime import datetime, timedelta

from PIL import Image, ImageTk

ACTIVATIONS = ['11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00']


def find_next_activation(hour, minute, activations):
    sorted_activations = sorted(activations)
    for a_hour, a_minute in sorted_activations:
        if a_hour < hour or (a_hour == hour and a_minute <= minute):
            continue
        return a_hour, a_minute
    return sorted_activations[0]


def get_time_text(hour, minute, second):
    if hour > 0:
        return f"{hour}:{minute:02d}:{second:02d}"
    if minute > 0:
        return f"{minute}:{second:02d}"
    return f"{second}"


class MaglySaver:
    activations = []
    first_activation = None
    activation_time_iter = 0

    def __init__(self, img_path, activation_times):
        self.parse_activation_times(activation_times)

        self.root = tk.Tk()
        self.root.title('Magly')
        self.root.attributes("-fullscreen", True)
        self.root.bind("<F11>",
                       lambda event: self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen")))
        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))
        self.root.update()

        self.width, self.height = self.root.winfo_width(), self.root.winfo_height()
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, background="black",
                                highlightthickness=0)
        self.canvas.pack()

        img = Image.open(img_path)
        img = img.resize((self.width, self.height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)

        self.label_id = self.canvas.create_text(self.width / 2, self.height*0.575, text=self.generate_label(),
                                                fill='#cfb76e', font=('Arial', 30))

        self.clock_update()
        self.root.mainloop()

    def parse_activation_times(self, activation_times):
        min_hour = 25
        for activation in sorted(activation_times):
            hour, minute = [int(val) for val in activation.split(':')]
            min_hour = min(hour, min_hour)
            self.activations.append((hour, minute))
        min_minute = min([minute for hour, minute in self.activations if hour == min_hour])
        self.first_activation = (min_hour, min_minute)

    def clock_update(self):
        self.canvas.itemconfig(self.label_id, text=self.generate_label())
        self.root.after(1000, self.clock_update)

    def generate_label(self):
        curr_datetime = datetime.now()
        a_hour, a_minute = find_next_activation(curr_datetime.hour, curr_datetime.minute, self.activations)
        a_datetime = curr_datetime.replace(hour=a_hour, minute=a_minute, second=0, microsecond=0)
        if a_datetime.time() < curr_datetime.time():
            a_datetime = a_datetime + timedelta(days=1)
        print(curr_datetime)
        print(a_datetime)
        diff = (a_datetime - curr_datetime).seconds
        hours = diff // 3600
        diff %= 3600
        minute = diff // 60
        second = diff % 60
        return get_time_text(hours, minute, second)


if __name__ == '__main__':
    saver = MaglySaver('assets/background.png', ACTIVATIONS)
