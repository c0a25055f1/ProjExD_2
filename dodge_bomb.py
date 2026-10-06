import os
import sys
import time
import pygame as pg
import random


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.Rect) -> tuple[bool,bool]:
    """
    引数:こうかとんまたは爆弾のrect
    戻り値：タプル(横方向判定結果,縦方向判定結果)
    下面外ならTrue/画面外ならFalse
    """
    yoko,tate = True, True
    if rect.left < 0 or WIDTH < rect.right:
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate = False
    return yoko, tate



def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する関数
    引数: screen (画面のSurface)
    戻り値: None
    """

    bg_surface = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bg_surface, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))

    bg_surface.set_alpha(150)

    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rct = text.get_rect()
    text_rct.center = WIDTH // 2, HEIGHT // 2
    bg_surface.blit(text, text_rct)

    kk_img = pg.image.load("fig/8.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 0.9)
    
    kk_rct_left = kk_img.get_rect()
    kk_rct_left.center = WIDTH // 2 - 250, HEIGHT // 2
    bg_surface.blit(kk_img, kk_rct_left)
    
    kk_rct_right = kk_img.get_rect()
    kk_rct_right.center = WIDTH // 2 + 250, HEIGHT // 2
    bg_surface.blit(kk_img, kk_rct_right)
    
 
    screen.blit(bg_surface, [0, 0])
    
    pg.display.update()
    time.sleep(5)
    



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx = +5
    vy = +5

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return   

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for k,tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1] 
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) !=(True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        
        bb_rct.move_ip(vx,vy)
        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
