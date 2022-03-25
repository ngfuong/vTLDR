import tkinter as tk
from tkinter import ttk
from tkinter import Text, Button, RIDGE
from tkinter import messagebox

from summary import predict
from scrape_utils import get_content


def is_url(url):
    if str(url).startswith("http://") or str(url).startswith("https://"):
        return True
    else:
        return False


def summarize():
    text = t1.get("1.0", "end-1c")
    type = input.get()

    if text == "":
        messagebox.showerror('Error', 'Empty input')
    else:
        t2.delete(1.0, 'end')
        summary_text = ""

        if type == "Manual":
            summary_text = predict(text)
        elif type == "URL":
            if is_url(text):
                content = get_content(text)
                t1.delete(1.0, 'end')
                t1.insert('end', content)

                summary_text = predict(content)
            else:
                messagebox.showerror('Error', 'URL should starts with http:// or https://')

        t2.insert('end', summary_text)


def clear():
    t1.delete(1.0, 'end')
    t2.delete(1.0, 'end')


root = tk.Tk()
root.title('vTLDR')
root.geometry('530x330')
root.maxsize(530, 330)
root.minsize(530, 330)

news = tk.StringVar()
input = ttk.Combobox(root,
                   width=20,
                   textvariable=news,
                   state='readonly',
                   font=('Arial', 12),
                   )

input['values'] = (
    'Manual',
    'URL',
)

input.place(x=30, y=70)
input.current(0)

summary = tk.StringVar()
output = ttk.Combobox(root,
                      width=20,
                      textvariable=summary,
                      state='readonly',
                      font=('Arial, 12'),
                      )
output['values'] = (
    'Summary',
)

output.place(x=290, y=70)
output.current(0)

t1 = Text(root,
          width=30,
          height=10,
          borderwidth=5,
          relief=RIDGE)
t1.place(x=10, y=100)

t2 = Text(root,
          width=30,
          heigh=10,
          borderwidth=5,
          relief=RIDGE)
t2.place(x=260, y=100)

summarize_button = Button(root,
                text="Summarize",
                relief=RIDGE,
                borderwidth=3,
                font=('verdana',10,'bold'),
                cursor='hand2',
                command=summarize,
                )
summarize_button.place(x=150, y=280)

clear_button = Button(root,
               text="Clear",
               relief=RIDGE,
               borderwidth=3,
               font=('verdana',10,'bold'),
               cursor='hand2',
               command=clear
               )
clear_button.place(x=280, y=280)

root.mainloop()
