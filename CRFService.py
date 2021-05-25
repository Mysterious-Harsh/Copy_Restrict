import os, sys, psutil, tempfile, shutil, time, re
import pygetwindow as gw
from threading import Thread
# from pywinauto.application import Application

# from win32ui import MessageBox
# filepath = ""
# filename = ""
# Tdir = ""
flag = True
# Pid = ""


def check_popup():
	global filepath, filename, Tdir

	try:
		winlist = gw.getAllTitles()
		mvb = list( filter( re.compile( "Microsoft Visual Basic" ).search, winlist ) )
		shr = list( filter( re.compile( "Share" ).search, winlist ) )
		cmd = list( filter( re.compile( "cmd.exe" ).search, winlist ) )
		cpt = list( filter( re.compile( "Command Prompt" ).search, winlist ) )
		sas = list( filter( re.compile( "Save As" ).search, winlist ) )
		wtm = list( filter( re.compile( "Task Manager" ).search, winlist ) )
		wps = list( filter( re.compile( "PowerShell" ).search, winlist ) )

		if "Save As" in winlist:
			return True, "Save As"
		elif "Microsoft Word" in winlist:
			return True, "Microsoft Word"
		elif "Save a Copy" in winlist:
			return True, "Save a Copy"
		elif "Remote Files" in winlist:
			return True, "Remote Files"
		elif "Export" in winlist:
			return True, "Export"
		elif "Export As" in winlist:
			return True, "Export As"
		elif "Email" in winlist:
			return True, "Email"
		elif "Open" in winlist:
			return True, "Open"
		elif "Folder Option" in winlist:
			return True, "Folder Option"
		elif "Temp" in winlist:
			return True, "Temp"
		elif "Save Drawing As" in winlist:
			return True, "Save Drawing As"
		elif "Save this file" in winlist:
			return True, "Save this file"
		elif "Run" in winlist:
			return True, "Run"
		elif "Windows" in winlist:
			return True, "Windows"
		elif Tdir in winlist:
			return True, Tdir
		elif wtm != [] or wps != []:
			for proc in psutil.process_iter():
				try:
					temp = [ 'Taskmgr.exe', 'taskmgr.exe', 'powershell.exe' ]
					if proc.name() in temp:
						proc.kill()
						print( 'kill' )
				except Exception:
					pass
			return False, None
		elif mvb != []:
			return True, mvb[ 0 ]
		elif shr != []:
			return True, shr[ 0 ]
		elif sas != []:
			return True, sas[ 0 ]
		elif cmd != []:
			return True, cmd[ 0 ]
		elif cpt != []:
			return True, cpt[ 0 ]

	except Exception as e:
		print( e )

	return False, None


def close_popup():
	global flag

	while flag:
		try:
			TF, winname = check_popup()
			if TF:
				window = gw.getWindowsWithTitle( winname )
				window[ 0 ].close()

		except:
			try:
				window[ 0 ].restore()
				window[ 0 ].minimize()
			except:
				pass

		time.sleep( 1 )
	print( "popup Successfully terminated" )

	sys.exit()


if __name__ == "__main__":
	# check_proc( sys.argv[ 1 ], int( sys.argv[ 2 ] ) )
	print( sys.argv )
	filepath = os.path.abspath( sys.argv[ 1 ] )
	filename = os.path.basename( sys.argv[ 1 ] )
	Tdir = os.path.dirname( filepath ).split( '\\' )[ -1 ]
	Pid = int( sys.argv[ 2 ] )
	T0 = Thread( target=close_popup )
	T0.start()

	while True:
		#  ( PName in ( p.name() for p in psutil.process_iter() ) )
		if not psutil.pid_exists( Pid ):
			flag = False
			for proc in psutil.process_iter():
				try:
					for item in proc.open_files():
						if filepath == item.path:
							proc.kill()
							print( "killed" )
							try:
								os.remove( filepath )
							except:
								pass
							for root, dirs, files in os.walk( tempfile.gettempdir() ):
								for name in files:
									try:
										os.remove( os.path.join( root, name ) )
									except:
										pass
								for name in dirs:
									try:
										shutil.rmtree( os.path.join( root, name ) )
									except:
										pass
							sys.exit()
				except:
					pass
			win = gw.getWindowsWithTitle( filename )
			if win == []:
				win = gw.getWindowsWithTitle( filename.split( '.' )[ 0 ] )
			try:
				if win != []:
					for i in win:
						i.close()
			except Exception as e:
				print( e )

			# try:
			# 	app = Application().connect( title_re=".*{}.*".format( filename.split( '.' )[ 0 ] ) )
			# 	win = app.windows()
			# 	# print( win )
			# 	app.kill( soft=False )
			# except:
			# 	pass

			try:
				os.remove( filepath )
			except:
				pass
			for root, dirs, files in os.walk( tempfile.gettempdir() ):
				for name in files:
					try:
						os.remove( os.path.join( root, name ) )
					except:
						pass
				for name in dirs:
					try:
						shutil.rmtree( os.path.join( root, name ) )
					except:
						pass
			sys.exit()
		time.sleep( 2 )
