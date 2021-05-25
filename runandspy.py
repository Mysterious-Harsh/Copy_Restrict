import subprocess
import os, time, sys
from striprtf.striprtf import rtf_to_text
import psutil
import tempfile
import pygetwindow as gw
import shutil
import pathlib
import re
from threading import Thread
import pyperclip as pc
from win32ui import MessageBox
from cryptography.fernet import Fernet
import pystray
from PIL import Image

filepath = None
filename = None
Tdir = None
pwd = None
PName = None
Pid = None
clip = None
flag = True
# Hash = None
SHPid = None
key = None
logger = None
filehandle = None
_cached_stamp = None
systray = None
T1 = None
T2 = None
T3 = None
T4 = None


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
		elif "AppData" in winlist:
			return True, "AppData"
		elif Tdir in winlist:
			return True, Tdir
		elif wtm != [] or wps != []:
			for proc in psutil.process_iter():
				try:
					temp = [ 'Taskmgr.exe', 'taskmgr.exe', 'powershell.exe' ]
					if proc.name() in temp:
						proc.kill()
						print( 'kill' )
				except:
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

		logger.debug( "check_popup : {}".format( e ) )

	return False, None


def close_popup():

	global flag, logger
	while flag:
		try:
			TF, winname = check_popup()
			if TF:
				window = gw.getWindowsWithTitle( winname )
				window[ 0 ].close()
		except Exception as e:
			logger.debug( e )

			try:
				# window = gw.getWindowsWithTitle( winname )
				window[ 0 ].restore()
				window[ 0 ].minimize()
			except Exception as e:
				logger.debug( "close_popup : {}".format( e ) )

		time.sleep( 0.4 )
	print( "popup Successfully terminated" )

	sys.exit()


def start_check():
	global filepath, Pid, PName
	# print( Pid, filepath )
	service = os.path.join( os.path.dirname( __file__ ), 'CRFService\\CRFService.exe' )
	# print( service )
	shp = subprocess.Popen( [ service, filepath, str( Pid ) ] )
	print( "CRFService started" )
	return shp.pid


def check_CRFService():
	global filepath, Pid, flag, SHPid, PName, T1, T2, T3
	while flag:
		try:
			if not psutil.pid_exists( SHPid ):
				service = os.path.join( os.path.dirname( __file__ ), 'CRFService\\CRFService.exe' )
				print( service )
				shp = subprocess.Popen( [ service, filepath, str( Pid ) ] )
				SHPid = shp.pid

			if not T1.is_alive():
				logger.info( "T1 dead" )
				T1 = Thread( target=close_popup )
				T1.start()

			if not T2.is_alive():
				logger.info( "T2 dead" )
				T2 = Thread( target=save )
				T2.start()

			if not T3.is_alive():
				logger.info( "T3 dead" )
				T3 = Thread( target=copy_restrict )
				T3.start()

		except Exception as e:
			logger.debug( "check_shp : {}".format( e ) )

		time.sleep( 4 )

	sys.exit()


def save():
	global filepath, filename, pwd, flag, key, _cached_stamp, filehandle
	f1 = Fernet( key[ 0 ] )
	f2 = Fernet( key[ 1 ] )

	while flag:
		if os.path.exists( filepath ):
			try:
				stamp = os.stat( filepath ).st_mtime
				if stamp != _cached_stamp:

					_cached_stamp = stamp
					with open( filepath, 'rb' ) as F:
						file_data = F.read()

					encrypted_data1 = f1.encrypt( file_data )
					encrypted_data = f2.encrypt( encrypted_data1 )

					filehandle.seek( 0 )
					filehandle.truncate()
					filehandle.write( key[ 0 ] + encrypted_data + key[ 1 ] )
					filehandle.flush()
					print( "Saved" )
					time.sleep( 1 )

			except Exception as e:
				logger.debug( "save : {}".format( e ) )
				try:
					tempkey = Fernet.generate_key()
					EF = Fernet( tempkey )
					# print( len( tempkey ) )

					Temp = os.path.join( os.path.dirname( __file__ ), 'Lostfiles' )
					File = Temp + '\\' + filename.split( '.' )[ 0 ] + '.lst'

					if not os.path.exists( Temp ):
						os.mkdir( Temp )

					if os.path.exists( File ):
						os.remove( File )

					with open( filepath, 'rb' ) as F:
						file_data = F.read()

					enc_data = EF.encrypt( file_data )
					with open( File, 'wb' ) as f:
						f.write( tempkey + enc_data )

					# os._exit( 0 )

				except Exception as e:
					logger.debug( "save_except : {}".format( e ) )
		else:
			logger.info( "Program Terminate file not fount" )
			Exit()
			# filehandle.close()
			# os._exit( 0 )

		time.sleep( 1 )
	print( "Save Successfully terminated" )
	sys.exit()


# def copy_restrict():
# 	global clip, flag, logger
# 	pc.copy( " " )
# 	while flag:
# 		try:
# 			data = pc.paste()
# 			if ( clip != data ):
# 				clip = data
# 				text = rtf_to_text( data )
# 				pc.copy( text )
# 		except:
# 			try:
# 				pc.copy( " " )
# 			except Exception as e:
# 				logger.debug( "copy_res : {}".format( e ) )

# 		time.sleep( 1.5 )
# 	print( "copy Successfully terminated" )


# 	sys.exit()
def copy_restrict():
	global clip, flag
	pc.copy( ' ' )
	while flag:
		try:
			data = pc.paste()
			if ( ' ' != data ):
				# clip = data
				# text = rtf_to_text( data )
				pc.copy( ' ' )

		except:
			try:
				pc.copy( ' ' )
			except:
				pass
			pass
		time.sleep( 1 )
	print( "copy Successfully terminated" )

	sys.exit()


def Exit():
	global flag, systray, filehandle
	try:
		systray.stop()
		filehandle.close()
		flag = False
		print( "exit" )
		name = filename.split( '.' )[ 0 ]
		win = gw.getWindowsWithTitle( filename )
		if win == []:
			win = gw.getWindowsWithTitle( name )
		try:
			if win != []:
				for i in win:
					i.close()
		except Exception as e:
			print( e )

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
	except Exception as e:
		logger.debug( "Exit : {}".format( e ) )
	os._exit( 0 )


def Show():
	try:
		print( filename )
		window = gw.getWindowsWithTitle( filename )
		print( window )
		window[ 0 ].minimize()
		window[ 0 ].restore()
	except Exception as e:
		logger.debug( e )
		try:
			name = filename.split( '.' )[ 0 ]
			print( name )
			window = gw.getWindowsWithTitle( name )
			print( window )
			window[ 0 ].minimize()
			window[ 0 ].restore()
		except Exception as e:
			logger.debug( e )


def system_tray():
	global systray, filename
	name = filename.split( '.' )[ 0 ]
	while gw.getWindowsWithTitle( name ) == []:
		time.sleep( 2 )

	image = Image.open( os.path.join( os.path.dirname( __file__ ), "images/icon.ico" ) )
	menu = pystray.Menu( pystray.MenuItem( 'Show', Show, default=True ), pystray.MenuItem( 'Exit', Exit ) )
	systray = pystray.Icon( "Copy Restrict - " + filename + ".crf", image, "Copy Restrict - " + filename, menu )
	systray.run()


def main( A, B, C, D, E, F ):
	try:
		global filepath, filename, Tdir, pwd, PName, Pid, clip, flag, SHPid, key, filehandle, logger, _cached_stamp, T1, T2, T3, T4, systray

		Temp = os.path.join( os.path.dirname( __file__ ), 'Lostfiles' )
		if not os.path.exists( Temp ):
			os.mkdir( Temp )
		filehandle = E
		logger = F
		# os.system( "attrib +s +h /s \"{}\\*.*\" && attrib +s +h \"{}\" ".format( Temp, Temp ) )

		subprocess.Popen( [ "attrib", "+s", "+h", "/s", "{}\\*.*".format( Temp ) ], shell=True )
		subprocess.Popen( [ "attrib", "+s", "+h", "{}".format( Temp ) ], shell=True )
		service = os.path.join( os.path.dirname( __file__ ), 'CRFService\\CRFService.exe' )

		if os.path.exists( service ):
			filepath = os.path.abspath( A )
			filename = os.path.basename( A )
			Tdir = os.path.dirname( filepath ).split( '\\' )[ -1 ]
			pwd = B
			PName = C
			key = D

			clip = " "
			Pid = os.getpid()
			_cached_stamp = os.stat( filepath ).st_mtime
			Pid = os.getpid()

			flag = True
			logger.info( "Main Thread Started" )
			SHPid = start_check()

			T1 = Thread( target=close_popup )
			T1.start()
			T2 = Thread( target=save )
			T2.start()
			T3 = Thread( target=copy_restrict )
			T3.start()
			T4 = Thread( target=check_CRFService )
			T4.start()
			T5 = Thread( target=system_tray )
			T5.start()
			start = time.time()
			PERIOD_OF_TIME = 90
			subprocess.call( [ filepath ], shell=True )
			name = filename.split( '.' )[ 0 ]
			while gw.getWindowsWithTitle( filename ) == [] or gw.getWindowsWithTitle( name ) == []:
				if time.time() > start + PERIOD_OF_TIME:
					break
				time.sleep( 5 )

			while gw.getWindowsWithTitle( filename ) != [] or gw.getWindowsWithTitle( name ) != []:

				time.sleep( 5 )

			flag = False

		else:
			MessageBox( 'CRFService.exe Not found !', 'Error' )
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
		print( "Terminated !" )
		logger.info( "Program Terminated !" )
		filehandle.close()
		if not flag:
			systray.stop()
		sys.exit()
	except Exception as e:
		print( e )
		filehandle.close()
		logger.debug( "Main : {}".format( e ) )
		sys.exit()


# python "E:\My_Projects\Copy Restrict V6\Copy Restrict.py" test.docx.crf