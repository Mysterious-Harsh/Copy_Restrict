from cryptography.fernet import Fernet
import gzip
import os, time, shutil
import psutil
import tempfile
import runandspy
import random
from win32ui import MessageBox
import sys
from convert2pdf import Convert2pdf
import re
import subprocess
import pygetwindow as gw
from tkinter import filedialog


class Decrypt:

	def __init__( self, logger ):
		self.logger = logger
		self.backupdir = os.path.join( os.path.dirname( __file__ ), 'Backup' )
		if not os.path.exists( self.backupdir ):
			os.mkdir( self.backupdir )

	def Backup( self, filepath ):
		try:
			shutil.copy2( filepath, os.path.join( self.backupdir, os.path.basename( filepath ) ) )
		except Exception as e:
			self.logger.debug( e )

	def decrypt( self, filepath, pwd, PName=None ):
		filename = os.path.basename( os.path.splitext( filepath )[ 0 ] )
		flag = False
		for proc in psutil.process_iter():
			try:
				for item in proc.open_files():
					if os.path.basename( filepath ) == os.path.basename( item.path ):
						flag = True
			except:
				pass

		if flag:
			try:
				print( filename )
				window = gw.getWindowsWithTitle( filename )
				print( window )
				window[ 0 ].minimize()
				window[ 0 ].restore()
			except Exception as e:
				self.logger.debug( e )
				try:
					name = filename.split( '.' )[ 0 ]
					print( name )
					window = gw.getWindowsWithTitle( name )
					print( window )
					window[ 0 ].minimize()
					window[ 0 ].restore()
				except Exception as e:
					self.logger.debug( e )
					MessageBox( "File is already Running !", "Running" )

			sys.exit()
		else:

			try:
				key = []
				filehandle = open( filepath, 'ab+' )
				filehandle.seek( 0 )
				data = filehandle.read()
				key.append( data[ : 44 ] )
				key.append( data[ -44 : ] )

				f1 = Fernet( key[ 0 ] )
				f2 = Fernet( key[ 1 ] )

				ln = len( data )
				encrypted_data = data[ 44 : ln - 44 ]

				decrypted_data2 = f2.decrypt( encrypted_data )
				decrypted_data = f1.decrypt( decrypted_data2 )

			except Exception as e:
				self.logger.debug( e )
				filehandle.close()
				sys.exit()
				# decrypted_data, key = self.version4( filepath )

			self.Backup( filepath )
			tdir = tempfile.mkdtemp()
			tfname = tdir + "/" + filename

			with open( tfname, "wb" ) as TF:
				TF.write( decrypted_data )

			subprocess.Popen( [ "attrib", "+s", "+h", "/s", "{}\\*.*".format( tdir ) ], shell=True )
			subprocess.Popen( [ "attrib", "+s", "+h", "{}".format( tdir ) ], shell=True )

			# os.system( "attrib +s +h \"{}\\*.*\" /s".format( tdir ) )
			# os.system( "attrib +s +h \"{}\"".format( tdir ) )

			runandspy.main( tfname, pwd, PName, key, filehandle, self.logger )

	def convtoorg( self, filepath, key, pwd, PName=None ):

		try:

			key = []
			filehandle = open( filepath, 'rb' )
			filehandle.seek( 0 )
			data = filehandle.read()
			key.append( data[ : 44 ] )
			key.append( data[ -44 : ] )
			# print( key )
			f1 = Fernet( key[ 0 ] )
			f2 = Fernet( key[ 1 ] )

			ln = len( data )
			encrypted_data = data[ 44 : ln - 44 ]

			decrypted_data2 = f2.decrypt( encrypted_data )
			decrypted_data = f1.decrypt( decrypted_data2 )
			filehandle.close()

		except Exception as e:
			self.logger.debug( e )
			# decrypted_data, key = self.version4( filepath )
			filehandle.close()
			sys.exit()

		filename = os.path.basename( os.path.splitext( filepath )[ 0 ] )

		tdir = filedialog.askdirectory( initialdir=os.getcwd(), title="Select Directory" )
		tfname = tdir + "/" + filename

		with open( tfname, "wb" ) as TF:
			TF.write( decrypted_data )

		MessageBox( "File is Converted to it's Original form !", "Done" )

	def crftopdf( self, filepath, key, root ):
		filename = os.path.basename( os.path.splitext( filepath )[ 0 ] )

		flag = False
		for proc in psutil.process_iter():
			try:
				for item in proc.open_files():
					if os.path.basename( filepath ) == os.path.basename( item.path ):
						flag = True
			except:
				pass

		if flag:

			MessageBox( "File is in Use !", "Running" )
			sys.exit()
		else:
			try:
				key = []
				filehandle = open( filepath, 'rb' )
				filehandle.seek( 0 )
				data = filehandle.read()
				key.append( data[ : 44 ] )
				key.append( data[ -44 : ] )
				# print( key )
				f1 = Fernet( key[ 0 ] )
				f2 = Fernet( key[ 1 ] )

				ln = len( data )
				encrypted_data = data[ 44 : ln - 44 ]

				decrypted_data2 = f2.decrypt( encrypted_data )
				decrypted_data = f1.decrypt( decrypted_data2 )
				filehandle.close()

			except Exception as e:
				self.logger.debug( e )
				# decrypted_data, key = self.version4( filepath )
				filehandle.close()

			tdir = tempfile.mkdtemp()
			tfname = tdir + "/" + filename

			with open( tfname, "wb" ) as TF:
				TF.write( decrypted_data )

			subprocess.Popen( [ "attrib", "+s", "+h", "/s", "{}\\*.*".format( tdir ) ], shell=True )
			# subprocess.Popen( [ "attrib", "+s", "+h", "{}".format( tdir ) ] )

			file, ext = os.path.splitext( tfname )
			if re.search( r"^.xl", ext ) or re.search( r"^.csv", ext ):
				e2p = Convert2pdf()
				e2p.Convert( "excel", tfname, root )
			elif re.search( r"^.doc", ext ):
				e2p = Convert2pdf()
				e2p.Convert( "word", tfname, root )


if __name__ == "__main__":
	de = Decrypt()
