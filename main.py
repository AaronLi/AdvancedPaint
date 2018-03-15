from pygame import *
import lib.windowedprogram
import programs.canvas.canvas, programs.toolbox.toolbox, programs.layers.layers
running = True
screen = display.set_mode((1480,800),RESIZABLE)
import lib.window, lib.deskenv
canvas = lib.window.Window(program=programs.canvas.canvas.Canvas)
toolbox = lib.window.Window(program=programs.toolbox.toolbox.Toolbox)
layers = lib.window.Window(program=programs.layers.layers.Layers, xPos = 1000)
desktop = lib.deskenv.DeskEnv(screen.get_size())
mouse.set_visible(False)
desktop.addWindow(canvas)
desktop.addWindow(toolbox)
desktop.addWindow(layers)
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
    screen.fill((170,170,170))

    desktop.draw(screen, mPos,mb)
    desktop.update(mPos,mb)

    display.flip()
    display.set_caption(str(clockity.get_fps()))
    oMPos = mPos
    clockity.tick(120)
quit()