import os
import sys
import time
import pygame as pg
import random

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し、真理値タプルを返す
    引数: こうかとんRectかばくだんRect
    戻り値: タプル(横方向判定結果, 縦方向判定結果)
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に、半透明の黒い画面と「Game Over」の文字、
    泣いているこうかとんを表示する関数
    引数: screen (画面のSurface)
    戻り値: None
    """
    # 黒い半透明の画面を作成して貼り付け
    bg_surface = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bg_surface, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    bg_surface.set_alpha(150)
    
    # 白文字のGame Overを作成
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rct = text.get_rect()
    text_rct.center = WIDTH // 2, HEIGHT // 2
    bg_surface.blit(text, text_rct)
    
    # 泣いているこうかとん画像をロードし、左右に配置
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


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    時間とともに拡大する爆弾の画像リストと加速度リストを生成する関数
    引数: なし
    戻り値: 爆弾Surfaceのリストと加速度リストのタプル
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
        
    return bb_imgs, bb_accs


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    移動量タプルと対応する画像Surfaceの辞書を生成する関数
    引数: なし
    戻り値: 押下キーに対する移動量の合計値タプルをキー、rotozoomしたSurfaceを値とする辞書
    """
    base_img = pg.image.load("fig/3.png")
    flip_img = pg.transform.flip(base_img, True, False)
    
    kk_dict = {
        (0, 0): pg.transform.rotozoom(flip_img, 0, 0.9),      # 停止(右向き)
        (0, -5): pg.transform.rotozoom(flip_img, 90, 0.9),    # 上
        (0, +5): pg.transform.rotozoom(flip_img, -90, 0.9),   # 下
        (-5, 0): pg.transform.rotozoom(base_img, 0, 0.9),     # 左
        (+5, 0): pg.transform.rotozoom(flip_img, 0, 0.9),     # 右
        (-5, -5): pg.transform.rotozoom(base_img, -45, 0.9),  # 左上
        (+5, -5): pg.transform.rotozoom(flip_img, 45, 0.9),   # 右上
        (-5, +5): pg.transform.rotozoom(base_img, 45, 0.9),   # 左下
        (+5, +5): pg.transform.rotozoom(flip_img, -45, 0.9),  # 右下
    }
    return kk_dict


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    
    kk_imgs = get_kk_imgs()
    bb_imgs, bb_accs = init_bb_imgs()

    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
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
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1] 
        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        kk_img = kk_imgs[tuple(sum_mv)]

        avx = vx * bb_accs[min(tmr//500, 9)]
        avy = vy * bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]

        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height

        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()