from pygame import *
running = True
screen = display.set_mode((1480,800),RESIZABLE)
import programs.toolbox.toolboxdata as toolboxdata
import lib.layerdata as layerData
import lib.window as window
import programs.canvas.canvas as canvas
import programs.layers.layers as layers
import programs.toolbox.toolbox as toolbox
import lib.deskenv as deskenv
tbData = toolboxdata.ToolboxData()
lData = layerData.LayerData()
canvasWin = window.Window(program=canvas.Canvas, programParameters={'toolboxData':tbData, 'layerData':lData})
toolboxWin = window.Window(program=toolbox.Toolbox, programParameters={'toolboxData':tbData})
layersWin = window.Window(program=layers.Layers, xPos = 1000, programParameters={'layerData':lData})
desktop = deskenv.DeskEnv(screen.get_size())
mouse.set_visible(False)
desktop.addWindow(canvasWin)
desktop.addWindow(toolboxWin)
desktop.addWindow(layersWin)
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