import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import ttk

def button_click(event):                   #ボタンが押されたときの処理
    btn = event.widget
    num = btn["text"]
    entry.grid(row=0,column=0,columnspan=3)#計算結果表示枠
    if num == "=":#計算結果を表示
        ans = entry.get()
        print(ans)
        res = eval(ans)
        entry.delete(0,tk.END)
        entry.insert(tk.END,res)
    elif num == "AC":                     #オールクリア/現在の計算式を全消しする
        entry.delete(0,tk.END)
    else:#計算式作成
        entry.insert(tk.END,num)

if __name__ == '__main__':                #main関数
    root = tk.Tk()
    root.geometry("400x600")
    root.title("電卓")
    entry = tk.Entry(root,justify="right",width=10,font=("Time New Roman",40))

    s,t = 1,0
    for i,num in enumerate(["AC"," "," ",  #計算ボタン
                            9, 8, 7,
                            6, 5, 4,
                            3, 2, 1,
                            0,"+","-",
                            "*","/","="]):
        btn = tk.Button(root,
                        text = f"{num}",
                        width = 4,
                        height = 2,
                        font = ("Time New Roman",30)
                        )
        btn.bind("<1>", button_click)     #計算結果ボタン並び替え
        btn.grid(row=s,column=t)
        t += 1
        if(i+1)%4 == 0:
            s += 1
            t = 0


    root.mainloop()