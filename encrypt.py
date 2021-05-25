from cryptography.fernet import Fernet
import subprocess
import platform
import os, time
import psutil
import tempfile
from win32ui import MessageBox


class Encrypt:

	def __init__( self, logger ):
		self.logger = logger

	def write_key( self ):

		key = Fernet.generate_key()
		with open( "key.key", "wb" ) as key_file:
			key_file.write( key )

	def encrypt( self, filename, pwd, save=None ):

		key1 = Fernet.generate_key()
		f1 = Fernet( key1 )
		key2 = Fernet.generate_key()
		f2 = Fernet( key2 )

		with open( filename, "rb" ) as file:
			file_data = file.read()

		encrypted_data1 = f1.encrypt( file_data )
		encrypted_data = f2.encrypt( encrypted_data1 )

		base = os.path.basename( filename )
		File = pwd + '/' + base + ".crf"

		with open( File, "wb" ) as f:
			f.write( key1 + encrypted_data + key2 )
			f.truncate()

		self.logger.info( "File Protected !" )
		if save == None:
			MessageBox( "File Protected !", "Done" )


if __name__ == "__main__":
	en = Encrypt()
	en.write_key()
