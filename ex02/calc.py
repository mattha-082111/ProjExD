import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import ttk

def button_click(event):
    btn = event.widget
    num = btn["text"]
    entry = tk.Entry(root,justify="right",width=10,font=("Time New Roman",40))
    entry.insert(tk.END,num)
    entry.grid(row=0,column=0,columnspan=3)
    if num == "=":#計算結果を表示
        ans = entry.get()
        res = eval(ans)
        entry.delete(tk.END,ans)
        entry.insert(tk.END,res)
    else:
        entry.insert(tk.END,ans)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("300x500")
    root.title("電卓")
    
    s,t = 1,0
    for i,num in enumerate([9, 8, 7,
                            6, 5, 4,
                            3, 2, 1,
                            0,"+","="]):
        btn = tk.Button(root,
                        text = f"{num}",
                        width = 4,
                        height = 2,
                        font = ("Time New Roman",30)
                        )
        btn.bind("<1>", button_click)
        btn.grid(row=s,column=t)
        t += 1
        if(i+1)%3 == 0:
            s += 1
            t = 0


    root.mainloop()

