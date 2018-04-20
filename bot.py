import cli
import gui
import shared

shared.init()

cliThread = cli.Cli()
cliThread.start()

gui = gui.Gui()
gui.run()

print('Exiting...')