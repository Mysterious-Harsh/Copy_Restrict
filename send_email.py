import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import os
from urllib.request import urlopen


class EmailApp:

	def __init__( self, master=None ):
		# build ui
		self.email_F = ttk.Frame( master )
		label_1_2 = ttk.Label( self.email_F )
		self.img_tentativesoftwarebackground766x766 = tk.PhotoImage( file='images/background.png' )
		label_1_2.config( background='#ffffff', image=self.img_tentativesoftwarebackground766x766, text='label_1_2' )
		label_1_2.place( anchor='nw', x='0', y='0' )
		from_L = ttk.Label( self.email_F )
		from_L.config( anchor='e', background='#ffffff', font='{Arial} 14 {bold}', text='From' )
		from_L.config( width='10' )
		from_L.grid( padx='10', pady='10' )
		self.from_E = ttk.Entry( self.email_F )
		self.from_E.config( font='{Arial} 12 {bold}', width='43' )
		self.from_E.grid( column='1', padx='10', pady='10', row='0' )
		to_L = ttk.Label( self.email_F )
		to_L.config( anchor='e', background='#ffffff', font='{Arial} 14 {bold}', text='To' )
		to_L.config( width='10' )
		to_L.grid( column='0', padx='10', pady='0', row='1' )
		self.to_list = tk.Listbox( self.email_F )
		self.to_list.config( activestyle='underline', font='{Arial} 12 {bold}', relief='flat', selectborderwidth='1' )
		self.to_list.config( selectmode='multiple', height=6, state='normal', takefocus=True, width='43' )
		self.to_list.grid( column='1', padx='10', pady='0', row='2' )
		label_3 = ttk.Label( self.email_F )
		label_3.config( anchor='e', background='#ffffff', font='{Arial} 14 {bold}', text='Subject' )
		label_3.config( width='10' )
		label_3.grid( column='0', padx='10', pady='5', row='3' )
		self.subject_E = ttk.Entry( self.email_F )
		self.subject_E.config( font='{Arial} 12 {bold}', width='43' )
		self.subject_E.grid( column='1', padx='10', pady='5', row='3' )
		label_4 = ttk.Label( self.email_F )
		label_4.config( anchor='e', background='#ffffff', font='{Arial} 14 {bold}', text='Attachment' )
		label_4.config( width='10' )
		label_4.grid( column='0', padx='10', pady='5', row='4' )
		self.attachment_E = ttk.Entry( self.email_F )
		self.attachment_E.config( font='{Arial} 12 {bold}', width='43', takefocus=True )
		self.attachment_E.grid( column='1', padx='10', pady='5', row='4' )
		self.attachment_E.bind( '<BackSpace>', self.remove_attachment, add='' )
		self.attachment_E.bind( '<Button-1>', self.add_attachment, add='' )
		self.attachment_E.bind( '<Delete>', self.remove_attachment, add='' )
		label_5 = ttk.Label( self.email_F )
		label_5.config( anchor='e', background='#ffffff', font='{Arial} 14 {bold}', text='Message' )
		label_5.config( width='10' )
		label_5.grid( column='0', padx='10', pady='0', row='5' )
		self.message_T = tk.Text( self.email_F )
		self.message_T.config( font='{Arial} 12 {bold}', height='10', insertunfocussed='none', maxundo='4' )
		self.message_T.config( relief='flat', state='normal', takefocus=True, undo='true' )
		self.message_T.config( width='43' )
		self.message_T.grid( column='1', padx='10', pady='0', row='6' )
		send_B = ttk.Button( self.email_F )
		send_B.config( text='Send' )
		send_B.grid( column='0', padx='10', pady='5', row='7' )
		send_B.configure( command=self.send )
		close_B = ttk.Button( self.email_F )
		close_B.config( text='Close' )
		close_B.grid( column='2', pady='5', row='7' )
		close_B.configure( command=self.close )
		self.count_L = ttk.Label( self.email_F )
		self.count_LTV = tk.StringVar( '' )
		self.count_L.config( anchor='w', background='#ffffff', font='{Arial} 12 {bold}', takefocus=False )
		self.count_L.config( text='0', textvariable=self.count_LTV, width='3' )
		self.count_L.grid( column='2', row='4' )
		self.count_LTV.set( 0 )
		self.email_F.config( height='790', relief='flat', takefocus=False, width='790' )
		self.email_F.place( anchor='nw', height='790', width='790', x='0', y='0' )

		# Main widget
		self.mainwindow = self.email_F
		self.emails = []
		for i in self.emails:
			self.to_list.insert( "end", i )
		self.attachments = []
		self.names = []

	def remove_attachment( self, event=None ):
		self.attachments.pop()
		self.names.pop()
		# self.attachment_E.config( state="enabled" )
		self.attachment_E.delete( 0, 'end' )
		self.attachment_E.insert( 0, ','.join( self.names ) )
		self.count_LTV.set( len( self.names ) )
		# self.attachment_E.config( state="readonly" )
		# print( self.attachments )
		# print( self.names )
		pass

	def add_attachment( self, event=None ):
		self.filename = filedialog.askopenfilename(
		    title="Select file", filetypes=( ( "all files", "*.*" ), ( "jpeg files", "*.jpg" ) )
		    )
		# print( self.filename )
		if self.filename != "":
			self.attachments.append( self.filename )
			self.names.append( os.path.basename( self.filename ) )
			# self.attachment_E.config( state="enabled" )
			self.attachment_E.delete( 0, 'end' )
			self.attachment_E.insert( 0, ','.join( self.names ) )
			self.count_LTV.set( len( self.names ) )
			# self.attachment_E.config( state="readonly" )
			# print( self.attachments )
			# print( self.names )
			pass

	def check_connection( self ):
		try:
			urlopen( 'https://www.google.com', timeout=2 )
			return True
		except:
			return False

	def send( self ):
		emails = self.to_list.curselection()
		if not self.check_connection():
			messagebox.showerror( "Offline", "Check Your Internet Connection !" )

		elif emails == ():
			messagebox.showerror( 'Invalid', "No Email ID Selected !" )
		elif self.from_E.get() == "":
			messagebox.showerror( 'Empty', "Please Enter Your Name in From field !" )
		else:
			try:
				fromaddr = "shilpeeconsultant1994@gmail.com"
				# toaddr = "EMAIL address of the receiver"

				# instance of MIMEMultipart
				msg = MIMEMultipart()

				# storing the senders email address
				msg[ 'From' ] = fromaddr

				# storing the receivers email address
				# msg[ 'To' ] = toaddr

				# storing the subject
				msg[ 'Subject' ] = self.subject_E.get()

				# string to store the body of the mail
				body = self.from_E.get() + " : \n" + self.message_T.get( "1.0", "end" )

				# attach the body with the msg instance
				msg.attach( MIMEText( body, 'plain' ) )

				# open the file to be sent
				for filename in self.attachments:
					# filename = "File_name_with_extension"
					try:
						attachment = open( filename, "rb" )

						# instance of MIMEBase and named as p
						p = MIMEBase( 'application', 'octet-stream' )

						# To change the payload into encoded form
						p.set_payload( ( attachment ).read() )

						# encode into base64
						encoders.encode_base64( p )

						p.add_header( 'Content-Disposition', "attachment; filename= %s" % os.path.basename( filename ) )

						# attach the instance 'p' to instance 'msg'
						msg.attach( p )
						# attachment.close()
					except Exception as e:
						print( e )

				# creates SMTP session
				s = smtplib.SMTP( 'smtp.gmail.com', 587 )

				# start TLS for security
				s.starttls()

				# Authentication
				s.login( fromaddr, "cafpudbwgemeevdr" )

				# Converts the Multipart msg into a string
				text = msg.as_string()

				for i in emails:
					try:
						# indicator.update(x+1)
						toaddr = self.emails[ i ]
						print( toaddr )
						msg[ 'To' ] = toaddr
						s.sendmail( fromaddr, toaddr, text )
					except Exception as e:
						print( e )
				messagebox.showinfo( "Success", "Mail Sent !" )
				# sending the mail
				# s.sendmail( fromaddr, toaddr, text )

				# terminating the session
				s.quit()
			except Exception as e:
				print( e )
				s.quit()
				messagebox.showerror( 'Error', e )

	def close( self ):
		self.email_F.destroy()

	def run( self ):
		self.mainwindow.mainloop()


if __name__ == '__main__':
	root = tk.Tk()
	app = EmailApp( root )
	app.run()
