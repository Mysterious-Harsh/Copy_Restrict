import tkinter as tk
import tkinter.ttk as ttk
from tkinter import ttk, filedialog, messagebox
from tkinter import *
from encrypt import Encrypt
from decrypt import Decrypt
import os
import sys
from win32ui import MessageBox
from convert2pdf import Convert2pdf
from threading import Thread
import re
from send_email import EmailApp
from request_key import Request_Key
from Validate import Validation
from check_registration import check_registration
import logging
from cryptography.fernet import Fernet

logging.basicConfig(
    filename=os.path.join( os.path.dirname( __file__ ), 'Logs.log' ),
    format='%(asctime)s %(message)s %(levelno)s %(threadName)s',
    filemode='a'
    )
logger = logging.getLogger()
logger.setLevel( logging.DEBUG )


class HomePage:

	def __init__( self, mainframe=None, master=None, PName=None ):

		self.root = master
		self.PName = PName
		self.Mainframe = mainframe
		if self.root != None:
			self.background_F = ttk.Frame( self.Mainframe )

			self.label_1 = ttk.Label( self.background_F )
			self.img_tentativesoftwarebackground3182020500x500 = tk.PhotoImage( file='images/background.png' )
			self.label_1.config(
			    background='#ffffff',
			    relief="flat",
			    image=self.img_tentativesoftwarebackground3182020500x500,
			    text='label_1'
			    )
			self.label_1.pack( expand='true', fill='y', side='top' )
			self.filepath_E = ttk.Entry( self.background_F )
			self.filepath_E.config( font='{Arial} 15 {bold}', state='normal', takefocus=False, width='30' )
			self.filepath_E.bind( "<Button-1>", self.add_attachment )
			self.filepath_E.place( anchor='n', relx='0.4', rely='0.18', x='0', y='0' )

			self.filepath_B = ttk.Button( self.background_F )
			self.filepath_B.config( takefocus=True, text='Select File', width='10' )
			self.filepath_B.place( anchor='n', relx='0.76', rely='0.18', x='0', y='0' )
			self.filepath_B.configure( command=self.add_attachment )

			self.encrypt_B = ttk.Button( self.background_F )
			self.encrypt_B.config( state="enabled", takefocus=True, text='Protect', width='10' )
			self.encrypt_B.place( anchor='n', relx='0.16', rely='0.42', x='0', y='0' )
			self.encrypt_B.configure( command=self.encrypt )

			self.decrypt_B = ttk.Button( self.background_F )
			self.decrypt_B.config( default='normal', text='Open', width='10' )
			self.decrypt_B.place( anchor='n', relx='0.89', rely='0.42', x='0', y='0' )
			self.decrypt_B.configure( command=self.decrypt )
			self.pdf_B = ttk.Button( self.background_F )
			self.img_pdffileicon30 = tk.PhotoImage( file='images/pdf-file-icon_30.png' )
			self.pdf_B.config(
			    compound='left', default='normal', image=self.img_pdffileicon30, state='normal', width='10'
			    )
			self.pdf_B.config( takefocus=True, text='PDF', width='6' )
			self.pdf_B.place( anchor='n', relx='0.16', rely='0.52', x='0', y='0' )
			self.pdf_B.configure( command=self.topdf )

			self.convtoorg_B = ttk.Button( self.background_F )
			self.convtoorg_B.config( compound='left', default='normal', state='normal', width='10' )
			self.convtoorg_B.config( takefocus=True, text='Conv. to Original', width='14' )
			self.convtoorg_B.place( anchor='n', relx='0.16', rely='0.62', x='0', y='0' )
			self.convtoorg_B.configure( command=self.convtoorg )

			self.openlostfile_B = ttk.Button( self.background_F )
			self.openlostfile_B.config( compound='left', default='normal', state='normal', width='10' )
			self.openlostfile_B.config( takefocus=True, text='Lost File' )
			self.openlostfile_B.place( anchor='n', relx='0.89', rely='0.62', x='0', y='0' )
			self.openlostfile_B.configure( command=self.lostfile )

			self.email_B = ttk.Button( self.background_F )
			self.img_email30 = tk.PhotoImage( file='images/email_30.png' )
			self.email_B.config( compound='left', default='normal', image=self.img_email30, state='normal', width='10' )
			self.email_B.config( takefocus=True, text='E-mail', width='6' )
			self.email_B.place( anchor='n', relx='0.89', rely='0.52', x='0', y='0' )
			self.email_B.configure( command=self.send_email )
			self.background_F.config( height='785', width='785' )
			self.background_F.pack( anchor='center', expand='true', fill='y', side='top' )
			self.filepath = ""

	def add_attachment( self, event=None ):
		self.filepath = filedialog.askopenfilename(
		    title="Select file",
		    filetypes=( ( "All Files", "*.*" ), ( "files", ".doc* .crf" ), ( "shp file", "*.crf" ) )
		    )
		if self.filepath != "":
			self.pwd = os.path.dirname( self.filepath )
			self.filepath_E.config( state="enabled" )
			self.filepath_E.delete( 0, "end" )
			self.filepath_E.insert( 0, os.path.basename( self.filepath ) )
			self.filepath_E.config( state="readonly" )
			pass

	def encrypt( self, file=None ):

		if file != None:
			self.filepath = file
			self.pwd = os.path.dirname( self.filepath )
		file, ext = os.path.splitext( self.filepath )
		if ( self.filepath == "" ):
			MessageBox( "No File Selected", "Error" )
		elif ( ext == '.crf' or ext == '.CRF' ):
			MessageBox( "File is already Protected", "Info" )
		else:
			en = Encrypt( logger )
			en.encrypt( self.filepath, self.pwd )

	def decrypt( self, file=None ):
		if file != None:
			self.filepath = file
			self.pwd = os.path.dirname( self.filepath )
		file, ext = os.path.splitext( self.filepath )
		file2, ext2 = os.path.splitext( file )
		if ( self.filepath == "" ):
			MessageBox( "No File Selected", "Error" )
		elif ( ext.lower() != '.crf' ):
			MessageBox( "Please Select .crf File", "Error" )
		elif ( ext2 == "" ):
			MessageBox( "Please Select Valid File, Like .doc.crf", "Error" )

		else:
			if self.root != None:
				self.root.destroy()
			de = Decrypt( logger )
			de.decrypt( self.filepath, self.pwd, self.PName )

	def lostfile( self, event=None ):
		file, ext = os.path.splitext( self.filepath )
		if ( self.filepath == "" ):
			MessageBox( "No File Selected", "Error" )
		elif ( ext != '.lst' ):
			MessageBox( "Please Select .lst File", "Error" )
		else:
			try:
				filehandle = open( self.filepath, 'rb' )
				filehandle.seek( 0 )
				data = filehandle.read()
				key = data[ : 44 ]
				enc_data = data[ 44 : ]
				F = Fernet( key )
				dec_data = F.decrypt( enc_data )
				base = os.path.basename( os.path.splitext( self.filepath )[ 0 ] )
				File = self.pwd + '/' + base
				with open( File, 'wb' ) as lstf:
					lstf.write( dec_data )
				logger.info( base + " File Recovered !" )
				MessageBox( "File Recovered !", "Success" )
			except Exception as e:
				logger.debug( e )

	def convtoorg( self ):

		file, ext = os.path.splitext( self.filepath )
		file2, ext2 = os.path.splitext( file )
		if ( self.filepath == "" ):
			MessageBox( "No File Selected", "Error" )
		elif ( ext != '.crf' ):
			MessageBox( "Please Select .crf File", "Error" )
		elif ( ext2 == "" ):
			MessageBox( "Please Select Valid File, Like .doc.crf", "Error" )

		else:
			de = Decrypt( logger )
			de.convtoorg( self.filepath, self.pwd, self.PName )

	def topdf( self ):
		file, ext = os.path.splitext( self.filepath )
		if ( self.filepath == "" ):
			MessageBox( "No File Selected", "Error" )
		elif ( ext == '.crf' ):
			de = Decrypt( logger )
			de.crftopdf( self.filepath, self.Mainframe, self.root )
		else:
			if re.search( r"^.xl", ext ) or re.search( r"^.csv", ext ):

				e2p = Convert2pdf()
				e2p.Convert( "excel", self.filepath, self.root )
			elif re.search( r"^.doc", ext ):

				e2p = Convert2pdf()
				e2p.Convert( "word", self.filepath, self.root )
			else:
				MessageBox( "Unsupported File Type !", "Error" )

	def send_email( self ):
		E = EmailApp( self.background_F )


# python "e:/My_Projects/Shilpee Group V5/Shilpee Group.py" "C:\Users\Kishan\Downloads\test.docx.crf"
# E:\My_Projects\Shilpee Group V4\Backup