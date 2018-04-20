import inputx
import gui
import shared

shared.init()

cliThread = inputx.Cli()
cliThread.start()

gui = gui.Gui()
gui.run()

print('Exiting...')