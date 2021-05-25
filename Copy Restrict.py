import tkinter as tk
import tkinter.ttk as ttk
from tkinter import ttk, filedialog, messagebox
from tkinter import *
import os
import sys
from win32ui import MessageBox
import re
from request_key import Request_Key
from Validate import Validation
from check_registration import check_registration
from home_page import HomePage


class Copy_Restrict:

	def __init__( self, master=None, PName=None ):
		self.root = master
		self.PName = PName
		if self.root != None:
			self.home = os.path.expanduser( '~' )
			self.filepath = os.path.join( self.home, "do_not_delete", "do_not_delete.key.enc" )
			# print( os.getcwd() )
			self.pwd = os.path.dirname( __file__ )
			self.filepath2 = os.path.join( self.pwd, "registration_key", "registration_key.key.crf" )
			# print( self.filepath )
			# print( self.filepath2 )
			self.Mainframe = ttk.Labelframe( self.root )
			self.root.title( "Copy Restrict" )
			self.root.tk.call( "wm", "iconphoto", self.root._w, PhotoImage( file="images/logo.png" ) )
			self.s_w = self.root.winfo_screenwidth()
			self.s_h = self.root.winfo_screenheight()
			self.wow = 1200
			self.how = 800
			x_c = ( ( self.s_w / 2 ) - ( self.wow / 2 ) )
			y_c = ( ( self.s_h / 2 ) - ( self.how / 2 ) )
			self.root.geometry( "%dx%d+%d+%d" % ( self.wow, self.how, x_c, y_c ) )
			self.root.update()
			self.Mainframe.config( height='200', text='Copy Restrict', width='200' )
			self.Mainframe.pack( expand='true', fill='both', side='top' )
			self.message_1 = tk.Message( self.Mainframe )
			self.message_1.config(
			    background='#ffffff',
			    font='{Arial} 11 {bold}',
			    relief='flat',
			    text='Developed By : Harsh Patel',
			    width='250'
			    )
			self.message_1.place( anchor='n', relx='0.91', rely='0.95', x='0', y='0' )
			self.mainwindow = self.Mainframe
			CR = check_registration()
			FLAG = CR.check()
			# print( FLAG )
			if os.path.exists( self.filepath ) and os.path.exists( self.filepath2 ) and FLAG:

				HP = HomePage( self.Mainframe, self.root, self.PName )
			else:
				self.register_F = ttk.Frame( self.Mainframe )
				label_1 = ttk.Label( self.register_F )
				self.img_tentativesoftwarebackground766x766 = tk.PhotoImage( file='images/background.png' )
				label_1.config( background='#ffffff', image=self.img_tentativesoftwarebackground766x766 )
				label_1.pack( expand='true', fill='y', side='top' )
				self.getkey_MTV = tk.StringVar()
				getkey_M = tk.Message( self.register_F )
				getkey_M.config(
				    background='#ffffff',
				    font='{Arial} 15 {bold}',
				    takefocus=False,
				    text='You Do not have a License Key.\nEnter Your Name.',
				    width='550',
				    textvariable=self.getkey_MTV
				    )
				self.getkey_MTV.set( 'You Do not have a License Key.\nEnter Your Name.' )
				getkey_M.place( anchor='n', relx='0.5', rely='0.42', x='0', y='0' )
				self.name_E = ttk.Entry( self.register_F )
				self.name_E.config( font='{Arial} 12 {bold}', takefocus=True, width='31' )
				self.name_E.place( anchor='n', relx='0.5', rely='0.52', x='0', y='0' )

				self.getkey_B = ttk.Button( self.register_F )
				self.getkey_B.config( text='Get Key' )

				self.getkey_B.configure( command=self.Get_Key )
				self.getkey_B.place( anchor='n', relx='0.5', rely='0.57', x='0', y='0' )

				self.register_F.config( height='768', width='768' )
				self.register_F.pack( anchor='center', expand='true', fill='y', side='top' )
				self.register_F.pack_propagate( 0 )

			self.config()

	def config( self ):
		self.filepath = ""

		# self.root.resizable( False, False )
		self.style = ttk.Style( self.mainwindow )
		self.style.configure( "TLabelframe", background="#ffffff", highlightthickness=5, relief="flat" )
		self.style.configure( "TFrame", background="#ffffff", highlightthickness=5, relief="flat" )
		self.style.configure(
		    "TLabelframe.Label",
		    background="#081944",
		    foreground="#ffffff",
		    font=( 'Arial', 18, 'bold' ),
		    width=self.wow,
		    anchor="center",
		    relief="flat"
		    )
		self.style.configure(
		    "Treeview",
		    fieldbackground="#ffffff",
		    background="#ffffff",
		    foreground="#000000",
		    font=( "Arial", 11, "bold" ),
		    borderwidth=5,
		    relief="flat"
		    )
		self.style.configure( "Treeview.Heading", font=( "Arial", 12, "bold" ) )

		self.style.configure(
		    "TButton",
		    background="#000000",
		    foreground="#000000",
		    font=( "Arial", 15, "bold" ),
		    relief="flat",
		    highlightcolor="blue",
		    bordercolor="#ffffff",
		    takefocus=True,
		    )
		# self.style.map( "TButton", background=[ ( 'active', 'blue' ) ] )
		self.style.configure(
		    "TLabel",
		    padding=0,
		    font=( "Arial", 11, "bold" ),
		    relief="flat",
		    width=14,
		    takefocus=False,
		    bordercolor="#ffffff",
		    cursor="arrow",
		    anchor="center"
		    )

		self.style.configure( "TEntry", fieldbackground="#99ddff", font=( "Arial", 15, "bold" ) )
		self.count = 0

	def Get_Key( self ):
		name = self.name_E.get()
		if name == "":
			messagebox.showerror( 'Empty', "Please Enter Your Name !" )
		else:

			self.getkey_MTV.set(
			    "Contact to Your Main Office and Ask for License Key.\nDo Not Close Window and Enter the Key."
			    )
			self.getkey_B.configure( command=self.verify_Key, text="Verify Key" )
			self.name_E.delete( 0, "end" )
			self.Validate = Validation( name )

	def verify_Key( self ):
		key = self.name_E.get()
		if key == "":
			messagebox.showerror( 'Empty', "Please Enter Key !" )
		else:
			self.flag = self.Validate.compare( key )
			if self.flag:
				CK = check_registration()
				CK.Register( key )
				self.register_F.destroy()
				HP = HomePage( self.Mainframe, self.root )
				# self.homepage()
			else:
				messagebox.showerror( 'Wrong', "Wrong Key !" )
				self.count = self.count + 1
				if self.count == 3:
					self.root.destroy()

		pass

	def run( self ):
		self.mainwindow.mainloop()


def args( file, PName ):
	filepath = os.path.abspath( file )
	PName = PName
	pwd = os.path.dirname( filepath )

	file, ext = os.path.splitext( os.path.basename( filepath ) )
	HP = HomePage( PName=PName )
	if ( filepath == "" ):
		MessageBox( "No File Selected", "Error" )
	elif ( ext == '.crf' or ext == '.CRF' ):
		HP.decrypt( filepath )
	else:
		HP.encrypt( filepath )
		# MessageBox( 'You are not able to protect files !', 'Restricted' )


if __name__ == '__main__':

	PName = os.path.basename( sys.argv[ 0 ] )
	if len( sys.argv ) == 1:
		root = tk.Tk()
		app = Copy_Restrict( root, PName )
		app.run()
	elif len( sys.argv ) == 2:
		home = os.path.expanduser( '~' )
		filepath = os.path.join( home, "do_not_delete", "do_not_delete.key.enc" )
		pwd = os.path.dirname( __file__ )

		if os.path.exists( filepath ):
			args( sys.argv[ 1 ], PName )

		else:
			MessageBox( 'You PC is not Registered !', "Error" )
