import pygame as pg
import sys
import random as ra
import tkinter as tk


class Screen: # 画面表示クラス
    def __init__(self, title, wh, image):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)     # Surface
        self.rct = self.sfc.get_rect()         # Rect
        self.bgi_sfc = pg.image.load(image)    # Surface
        self.bgi_rct = self.bgi_sfc.get_rect() # Rect

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)

class Zanki:
    def __init__(self, image:str,size: float, vxy):
        self.sfc = pg.image.load(image) 
        self.sfc = pg.transform.rotozoom(self.sfc, 0, size)
        self.rct = self.sfc.get_rect() # Rect
        self.vx, self.vy = vxy

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen):
        self.blit(scr)


class Bird: # こうかとんに関するクラス
    def __init__(self, image: str, size: float, xy):
        self.sfc = pg.image.load(image)                      # Surface
        self.sfc = pg.transform.rotozoom(self.sfc, 0, size)  # Surface
        self.rct = self.sfc.get_rect()                       # Rect
        self.rct.center = xy

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen):
        key_states = pg.key.get_pressed() # 辞書
        if key_states[pg.K_UP]: 
            self.rct.centery -= 1
        if key_states[pg.K_DOWN]: 
            self.rct.centery += 1
        if key_states[pg.K_LEFT]: 
            self.rct.centerx -= 1
        if key_states[pg.K_RIGHT]: 
            self.rct.centerx += 1
        
        if check_bound(self.rct, scr.rct) != (1, 1): # 領域外だったら
            if key_states[pg.K_UP]: 
                self.rct.centery += 1
            if key_states[pg.K_DOWN]: 
                self.rct.centery -= 1
            if key_states[pg.K_LEFT]: 
                self.rct.centerx += 1
            if key_states[pg.K_RIGHT]: 
                self.rct.centerx -= 1
        self.blit(scr)

    def attack(self):
        return Shot(self)   


class Bomb: #爆弾に関するクラス
    def __init__(self, color, size, vxy, scr: Screen):
        self.sfc = pg.Surface((2*size, 2*size))             # Surface
        self.sfc.set_colorkey((0, 0, 0)) 
        pg.draw.circle(self.sfc, color, (size, size), size)
        self.rct = self.sfc.get_rect()                      # Rect
        self.rct.centerx = ra.randint(0, scr.rct.width)
        self.rct.centery = ra.randint(0, scr.rct.height)
        self.vx, self.vy = vxy 

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen):
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate   
        
        self.blit(scr) 


class Shot: # ビームに関するクラス
    def __init__(self, chr: Bird):
        self.sfc = pg.image.load("fig/beam.png")
        self.sfc = pg.transform.rotozoom(self.sfc, 0, 0.1)
        self.rct = self.sfc.get_rect()
        self.rct.midleft = chr.rct.center

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen):
        self.rct.move_ip(+10, 0)
        self.blit(scr)
        if check_bound(self.rct, scr.rct) != (1,1):
            del self

'''
制作した機能 / 担当者
爆弾を複数個にする(ランダムで５個から２５個爆弾が出現) / 吉村
ランダムで爆弾の色が変化する / 岩田
こうかとんがビームを出せるようになる / 吉村
爆弾にビームを当てたら爆弾が消える / 吉村
ゲームオーバー・ゲームクリアになるとゲームを終了させる / 岩田
BGM・SEを流れるようにする / 松木・田畑・山本
制限時間設定 / 岩田
こうかとんの画像切り替え / 岩田
爆弾のサイズをランダムで設定 / 吉村
'''
def main(): # main関数
    global counter,cnt,hoge,BOMB_COUNT,SPEED
    clock = pg.time.Clock()
    scr = Screen("fighting!こうかとん", (1400, 700), "fig/pg_bg.jpg")
    kkt = Bird(f"fig/{cnt}.png", 2.0, (200, 500))
    bgn = int(pg.time.get_ticks())
    clock = pg.time.Clock()
    fonto = pg.font.Font("C:\WINDOWS\FONTS\BIZ-UDMINCHOM.TTC", 80)
    
    BOMB_COUNT = ra.randrange(5,15)
    SPEED = ra.randrange(1,2)
    bombs = [0 for c in range(BOMB_COUNT)]
    
    # 爆弾を表示
    bombs = [
            Bomb((ra.randint(0,255),(ra.randint(0,255)),
            (ra.randint(0,255))), ra.randint(10,25), 
            (+(SPEED),+(SPEED)), scr) for i in range(BOMB_COUNT)
            ]
    
    if BOMB_COUNT <= 7:
        pg.mixer.music.load("fig/mp3_BGM.mp3")                      #ゲームプレイ中常に楽しげなBGMが流れるようにする(爆弾が七個以下のとき)
        pg.mixer.music.play(2)
    else:
        pg.mixer.music.load("fig/Dear_Sir_Einstein.mp3")            #ゲームプレイ中常に殺伐としたBGMが流れるようにする(爆弾が八個以上のとき)
        pg.mixer.music.play(2)

    beam = None

    bombs_flag = [1 for d in range(BOMB_COUNT)]


    while True:
        scr.blit()

        sec = int(10 - (pg.time.get_ticks() - bgn) / 1000)           #秒数の計算
        if sec == 0:#制限時間が0のときゲームオーバー
            pg.mixer.music.load("fig/deathse.mp3")
            pg.mixer.music.play(1)
            Continue()
        txt = fonto.render(f"制限時間{sec}", True, (255,0,0))         #こうかとんの画像変更
        scr.sfc.blit(txt, (200, 100))    

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                hit_music = pg.mixer.Sound("fig/hit.mp3")
                hit_music.play()
                return
            #スペースキーでこうかとんがビームを発射する
            if (event.type == pg.KEYDOWN) and (event.key == pg.K_SPACE):
                beam = kkt.attack()                                    
                beam_music = pg.mixer.Sound("fig/mp3_006.wav")#
                beam_music.play()

        if beam:
            beam.update(scr)
            #ビームを爆弾に当てたときbombs_flagのパラメータを0にする
            for g in range(BOMB_COUNT):
                if bombs[g].rct.colliderect(beam.rct):
                    hit = pg.mixer.Sound("fig/爆発2.mp3")
                    hit.play()
                    bombs_flag[g] = 0
            
        #こうかとんが爆弾に当たった時、ゲームを強制終了する
        for k in range(BOMB_COUNT):
            if kkt.rct.colliderect(bombs[k].rct):
                hit2 = pg.mixer.Sound("fig/爆発2.mp3")
                hit2.play()
                pg.mixer.music.load("fig/deathse.mp3")
                pg.mixer.music.play(1)
                Continue() 
        kkt.update(scr)

        # #ビームを爆弾に当てた時に更新をしないようにする処理
        for e in range(BOMB_COUNT):
            if bombs_flag[e] != 0:
                bombs[e].update(scr)
        
        #爆弾のパラメータの合計値が0のときゲームを終了する
        if sum(bombs_flag) == 0:
            pg.mixer.music.load("fig/victory.mp3")
            pg.mixer.music.play(1)
            clear()
            
        pg.display.update()
        clock.tick(1000)

def Continue():#gameover画面(y/n) yの場合コンティニュー、nの場合ゲームを終了
    global root
    root = tk.Tk()
    root.geometry("220x100")
    root.title("GameOver")
    label = tk.Label(root, text="continue?", font = ("Times New Roman", 40))
    label.place(y = 90)
    label.pack()
    btn1 = tk.Button(root, text = "Yes", command = reset)
    btn1.place(x = 63, y = 60)
    btn2 = tk.Button(root, text = "No", command = exit)
    btn2.place(x = 126, y = 60)
    root.mainloop()

def clear():#ゲームクリアしたときの処理
    global root
    root = tk.Tk()
    root.geometry("400x110")
    root.title("ゲームクリア！")
    label = tk.Label(root, text="Congratulations!", font = ("Times New Roman", 40))
    label.place(y = 90)
    label.pack()
    btn = tk.Button(root, text = "おめでとう！", command = exit)
    btn.place(x = 150, y = 65)
    root.mainloop()

def reset():#鳥のカウントとゲームオーバー画面の非表示　こうかとんの位置リセット　画像チェンジ
    global root,cnt
    cnt += 1
    if cnt == 9:
        cnt = 0
    root.destroy()
    pg.init()
    main()

def exit():#終了
    pg.quit()
    sys.exit()

def check_bound(rct, scr_rct):#[1] rct: こうかとん or 爆弾のRect    [2] scr_rct: スクリーンのRect
    yoko, tate = +1, +1 # 領域内
    if rct.left < scr_rct.left or scr_rct.right  < rct.right : yoko = -1 # 領域外
    if rct.top  < scr_rct.top  or scr_rct.bottom < rct.bottom: tate = -1 # 領域外
    return yoko, tate


if __name__ == "__main__":
    cnt = 0
    fcnt = 0
    pg.init()
    main()
    while True:
        Continue()