import pygame as pg
import sys
import random


class Screen: # 画面表示クラス
    def __init__(self, title, wh, image):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)     # Surface
        self.rct = self.sfc.get_rect()         # Rect
        self.bgi_sfc = pg.image.load(image)    # Surface
        self.bgi_rct = self.bgi_sfc.get_rect() # Rect

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)


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
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = random.randint(0, scr.rct.height)
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

def main(): # main関数
    clock = pg.time.Clock()
    scr = Screen("fighting!こうかとん", (1600, 900), "fig/pg_bg.jpg")
    kkt = Bird("fig/6.png", 2.0, (900, 400))
    
    # 9つの爆弾を表示(この下以降が担当箇所)
    bkd1 = Bomb((random.randint(0,255),(random.randint(0,255)),(random.randint(0,255))), 10, (+1,+1), scr)
    bkd2 = Bomb((random.randint(0,255),(random.randint(0,255)),(random.randint(0,255))), 10, (+1,+1), scr)
    bkd3 = Bomb((random.randint(0,255),(random.randint(0,255)),(random.randint(0,255))), 10, (+1,+1), scr)
    bkd4 = Bomb((random.randint(0,255),(random.randint(0,255)),(random.randint(0,255))), 10, (+1,+1), scr)
    bkd5 = Bomb((random.randint(0,255),(random.randint(0,255)),(random.randint(0,255))), 10, (+1,+1), scr)
    bkd6 = Bomb((random.randint(0,255),(random.randint(0,255)),(random.randint(0,255))), 10, (+1,+1), scr)
    bkd7 = Bomb((random.randint(0,255),(random.randint(0,255)),(random.randint(0,255))), 10, (+1,+1), scr)
    bkd8 = Bomb((random.randint(0,255),(random.randint(0,255)),(random.randint(0,255))), 10, (+1,+1), scr)
    bkd9 = Bomb((random.randint(0,255),(random.randint(0,255)),(random.randint(0,255))), 10, (+1,+1), scr)

    beam = None

    bombs = [1,1,1,1,1,1,1,1,1]

    while True:
        scr.blit()

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            if (event.type == pg.KEYDOWN) and (event.key == pg.K_SPACE):
                beam = kkt.attack()
                beam_music = pg.mixer.Sound("fig/mp3_006.wav")
                beam_music.play()                                     #スペースキーでこうかとんが攻撃


        if beam:
            beam.update(scr)
            #ビームを爆弾に当てたときbombsのパラメータを0にする
            if bkd1.rct.colliderect(beam.rct):
                bombs[0] = 0
            if bkd2.rct.colliderect(beam.rct):
                bombs[1] = 0
            if bkd3.rct.colliderect(beam.rct):
                bombs[2] = 0
            if bkd4.rct.colliderect(beam.rct):
                bombs[3] = 0
            if bkd5.rct.colliderect(beam.rct):
                bombs[4] = 0
            if bkd6.rct.colliderect(beam.rct):
                bombs[5] = 0
            if bkd7.rct.colliderect(beam.rct):
                bombs[6] = 0
            if bkd8.rct.colliderect(beam.rct):
                bombs[7] = 0
            if bkd9.rct.colliderect(beam.rct):
                bombs[8] = 0
        #こうかとんが爆弾に当たった時、ゲームを強制終了する
        if kkt.rct.colliderect(bkd1.rct):
            return
        if kkt.rct.colliderect(bkd2.rct):
            return
        if kkt.rct.colliderect(bkd3.rct): 
            return
        if kkt.rct.colliderect(bkd4.rct):
            return
        if kkt.rct.colliderect(bkd5.rct):
            return
        if kkt.rct.colliderect(bkd6.rct):
            return
        if kkt.rct.colliderect(bkd7.rct):
            return
        if kkt.rct.colliderect(bkd8.rct):
            return
        if kkt.rct.colliderect(bkd9.rct):
            return
        
        kkt.update(scr)
        #ビームを爆弾に当てた時に更新をしないようにする処理
        if bombs[0] != 0:
            bkd1.update(scr)
        if bombs[1] != 0:
            bkd2.update(scr)
        if bombs[2] != 0:
            bkd3.update(scr)
        if bombs[3] != 0:
            bkd4.update(scr)
        if bombs[4] != 0:
            bkd5.update(scr)
        if bombs[5] != 0:
            bkd6.update(scr)
        if bombs[6] != 0:
            bkd7.update(scr)
        if bombs[7] != 0:
            bkd8.update(scr)
        if bombs[8] != 0:
            bkd9.update(scr)
        
        #爆弾のパラメータの合計値が0のときゲームを終了する
        if sum(bombs) == 0:
            return
            
        pg.display.update()
        clock.tick(1000)

def check_bound(rct, scr_rct):
    '''
    [1] rct: こうかとん or 爆弾のRect
    [2] scr_rct: スクリーンのRect
    '''
    yoko, tate = +1, +1 # 領域内
    if rct.left < scr_rct.left or scr_rct.right  < rct.right : yoko = -1 # 領域外
    if rct.top  < scr_rct.top  or scr_rct.bottom < rct.bottom: tate = -1 # 領域外
    return yoko, tate


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()