import tkinter
import tkinter as Tk
import maze_maker as mm

def key_down(event):
    global key
    key = event.keysym

def key_up():
    global key
    key = ""

def main_proc():
    global cx, cy,mx,my
    delta = { #押されているキーkey/値:移動幅リスト[x,y]
        ""      :[0,0],
        "Up"    :[0, -1],
        "Down"  :[0, +1],
        "Left"  :[-1, 0],
        "Right" :[+1,0],
        
    }
    try:
        #cx,cy = cx + delta[key][0], cy + delta[key][1]
        
        if maze_bg[my+delta[key][1]][mx+delta[key][0]] == 0:
            my,mx = my+delta[key][1],mx+delta[key][0]
    except:
        pass
    cx,cy = 100*mx+50,100*my+50
    canvas.coords("tori", cx, cy)
    root.after(150, main_proc)


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("迷えるこうかとん")

    canvas = Tk.Canvas(root,width=1500,height=900,bg="black")
    canvas.pack()
    maze_bg = mm.make_maze(15,9)#1:壁/0:床を生成する
    mm.show_maze(canvas,maze_bg)

    tori = Tk.PhotoImage(file = "fig/7.png")
    mx,my = 1,1
    cx,cy = 100*mx+50,100*my+50
    canvas.create_image(cx,cy,image=tori,tag="tori")

    key = ""

    main_proc()
    
    root.bind("<KeyPress>",key_down)
    root.bind("<KeyRelease>",key_up)
    root.mainloop()