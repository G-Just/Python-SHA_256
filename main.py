import SHA
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

font1 = ('Consolas', 20, 'normal')
font2 = ('Consolas', 10, 'normal')

root = tk.Tk()
root.title('SHA-256 Encryption')

canvas = tk.Canvas(root, height=500, width=900, bg='#161717')
canvas.pack()

input_box = Text(canvas, font=font1)
input_box.place(width=300, height=100, relx=1 / 3, rely=0.6)

button = Button(canvas, text='Encrypt using SHA-256 function', font=font2, bg='#125780', fg='white',
                command=lambda: [SHA.sha_256(input_box.get('1.0',END)), get_result()])
button.place(height=50, width=300, relx=1 / 3, y=430)

img = ImageTk.PhotoImage(Image.open('image.png').resize((300, 200), Image))
lab = Label(canvas, image=img)
lab.place(relx=1 / 3, y=20)

output = Label(canvas, text='', bg='#161717', fg='white', font=font2)
output.place(width=900, relx=0, rely=0.5)


def get_result():
    if not SHA._failed:
        output.config(text=f'Hash : {SHA.end_result}')
    else:
        output.config(text=SHA._failed_msg)


root.mainloop()
