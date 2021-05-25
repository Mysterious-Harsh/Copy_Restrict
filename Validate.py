import string
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import hashlib
from win32ui import MessageBox
from urllib.request import urlopen
import logging
import os


class Validation:

	def __init__( self, name ):
		logging.basicConfig(
		    filename=os.path.join( os.path.dirname( __file__ ), 'Logs.log' ),
		    format='%(asctime)s %(message)s %(levelno)s %(threadName)s',
		    filemode='a'
		    )
		self.logger = logging.getLogger()
		self.logger.setLevel( logging.DEBUG )
		self.res = ''.join(
		    random.choices( string.ascii_uppercase + string.ascii_lowercase + string.digits, k=24 )
		    )
		print( "The generated random string : " + str( self.res ) )
		self.name = name
		# if self.check_connection():
		try:

			# fromaddr = "shilpeeconsultant1994@gmail.com"
			# toaddr = "viren_shilpee@yahoo.co.in"
			fromaddr = "tinfo438@gmail.com"
			toaddr = "kishanpatel31199@gmail.com"

			# instance of MIMEMultipart
			msg = MIMEMultipart()

			# storing the senders email address
			msg[ 'From' ] = fromaddr

			# storing the receivers email address
			msg[ 'To' ] = toaddr

			# storing the subject
			msg[ 'Subject' ] = "Key"

			# string to store the body of the mail
			body = self.name + " --> " + self.res

			# attach the body with the msg instance
			msg.attach( MIMEText( body, 'plain' ) )

			s = smtplib.SMTP( 'smtp.gmail.com', 587 )

			# start TLS for security
			s.starttls()

			# Authentication
			# s.login( fromaddr, "cafpudbwgemeevdr" )
			s.login( fromaddr, "password" )

			# Converts the Multipart msg into a string
			text = msg.as_string()

			# sending the mail
			s.sendmail( fromaddr, toaddr, text )

			# terminating the session
			s.quit()
			MessageBox( "Requested for Key !", "Sent" )
		except Exception as e:
			self.logger.debug( "Validation : {}".format( e ) )
			print( e )
			MessageBox( str( e ), "error" )
			# s.quit()

		# else:
		# 	MessageBox( "Check Your Internet Connection !", "Offline" )

	# def check_connection( self ):
	# 	try:
	# 		urlopen( 'https://www.google.com', timeout=4 )
	# 		return True
	# 	except:
	# 		return False

	def compare( self, license_key ):
		temp = []
		hash_key = hashlib.md5(
		    hashlib.sha1(
		        hashlib.sha256( hashlib.sha512( self.res.encode() ).hexdigest().encode()
		                       ).hexdigest().encode()
		        ).hexdigest().encode()
		    ).hexdigest()
		for i, j in zip( [ 0, 8, 16, 24 ], [ 8, 16, 24, 32 ] ):
			temp.append( hash_key[ i : j ] )
		key = '-'.join( temp )

		if license_key == key:
			return True
		else:
			False

		print( temp )

		pass


# v = Validation()
# print(hashlib.algorithms_available)
# print(hashlib.algorithms_guaranteed)