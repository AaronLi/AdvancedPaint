from pygame import *
import lib.window, lib.deskenv

running = True
screen = display.set_mode((1280,720),RESIZABLE)
canvas = lib.window.Window()
testWindow2 = lib.window.Window("Heyyo Big window",70,70,400,200)
desktop = lib.deskenv.DeskEnv(screen.get_size())
desktop.addWindow(canvas)
desktop.addWindow(testWindow2)
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
            desktop.resize(e.size)
    mPos = mouse.get_pos()
    mb = mouse.get_pressed()
    screen.fill((255,255,255))

    desktop.draw(screen, mPos,mb)
    desktop.update(mPos,mb)

    display.flip()
    oMPos = mPos
quit()