from pygame import *

running = True
screen = display.set_mode((1280,720),RESIZABLE)
import lib.window, lib.deskenv
canvas = lib.window.Window("Super long window name that won't fit into anything")
testWindow2 = lib.window.Window("Heyyo Big Small window",70,70,400,200)
desktop = lib.deskenv.DeskEnv(screen.get_size())
mouse.set_visible(False)
desktop.addWindow(canvas)
desktop.addWindow(testWindow2)
clockity = time.Clock()
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
    clockity.tick(60)
quit()