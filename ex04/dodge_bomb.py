import pygame as pg
import sys
import random

def main():
    clock = pg.time.Clock()

    #練習1
    pg.display.set_caption("逃げろ！こうかとん")
    screen_sfc = pg.display.set_mode((1300, 700))
    screen_rct = screen_sfc.get_rect()
    bgimg_sfc = pg.image.load("pg_bg.jpg")
    bgimg_rct = bgimg_sfc.get_rect()
    screen_sfc.blit(bgimg_sfc, bgimg_rct)

    #練習3
    kkimg_sfc = pg.image.load("fig/6.png")
    kkimg_sfc = pg.transform.rotozoom(kkimg_sfc, 0, 2.0)
    kkimg_rct = kkimg_sfc.get_rect()
    kkimg_rct.center = 600, 300

    #練習5
    bmimg_sfc = pg.Surface((20, 20))
    bmimg_sfc.set_colorkey((0, 0, 0))
    pg.draw.circle(bmimg_sfc, (255, 0, 0),(10, 10), 10)
    bmimg_rct = bmimg_sfc.get_rect()
    bmimg_rct.centerx = random.randint(0, screen_rct.width)
    bmimg_rct.centery = random.randint(0, screen_rct.height)

    #練習6
    vx, vy = +1, +1

    while(1):
        screen_sfc.blit(bgimg_sfc, bgimg_rct)

        #練習2
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        #練習4
        key_states = pg.key.get_pressed()
        if key_states[pg.K_UP]     == True :kkimg_rct.centery -= 1
        if key_states[pg.K_DOWN]   == True :kkimg_rct.centery += 1
        if key_states[pg.K_LEFT]   == True :kkimg_rct.centerx -= 1
        if key_states[pg.K_RIGHT]  == True :kkimg_rct.centerx += 1

        #練習7
        if check_bound(kkimg_rct, screen_rct) != (1, 1):
            if key_states[pg.K_UP]     == True :kkimg_rct.centery += 1
            if key_states[pg.K_DOWN]   == True :kkimg_rct.centery -= 1
            if key_states[pg.K_LEFT]   == True :kkimg_rct.centerx += 1
            if key_states[pg.K_RIGHT]  == True :kkimg_rct.centerx -= 1

        screen_sfc.blit(kkimg_sfc, kkimg_rct)

        #練習6
        bmimg_rct.move_ip(vx, vy)

        #練習5
        screen_sfc.blit(bmimg_sfc, bmimg_rct)

        #練習7
        yoko, tate = check_bound(bmimg_rct, screen_rct)
        vx *= yoko
        vy *= tate

        #練習8
        if kkimg_rct.colliderect(bmimg_rct): return

        pg.display.update()
        clock.tick(1000)

def check_bound(rct, scr_rct):
    yoko, tate = +1, +1
    if rct.left < scr_rct.left or scr_rct.right < rct.right     : yoko = -1
    if rct.top  < scr_rct.top  or scr_rct.bottom < rct.bottom   : tate = -1
    return yoko, tate

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()