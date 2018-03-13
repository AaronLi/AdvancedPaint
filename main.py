from pygame import *
import lib.window

running = True
screen = display.set_mode((1280,720),RESIZABLE)
canvas = lib.window.Window()
windows = []
while running:
    for e in event.get():
        if e.type==QUIT:
            running=False
        elif e.type==MOUSEBUTTONDOWN:
            oMPos = e.pos
        elif e.type==MOUSEBUTTONUP:
            pass
        elif e.type == VIDEORESIZE:
            screen = display.set_mode(e.size,RESIZABLE)
    mPos = mouse.get_pos()
    mb = mouse.get_pressed()
    screen.fill((255,255,255))

    canvas.draw(screen,mPos,mb)
    canvas.update(mPos,mb,Rect(0,0,screen.get_width(),screen.get_height()-40))

    display.flip()
    oMPos = mPos
quit()