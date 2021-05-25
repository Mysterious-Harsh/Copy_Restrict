from pywinauto.application import Application


def force_close():
	app = Application().connect( title_re="hello" )
	win = app.windows()
	print( win )
	app.kill( soft=False )
