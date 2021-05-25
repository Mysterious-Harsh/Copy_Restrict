# from docx2pdf import convert
from tkinter import ttk, filedialog, messagebox
import os, shutil, tempfile
from win32com import client
import win32api
import tkinter as tk
import tkinter.ttk as ttk
import tempfile


class Convert2pdf:

	def Convert( self, filetype, filepath=None, master=None ):
		self.filepath = os.path.abspath( filepath )
		self.filename = os.path.basename( self.filepath ).split( '.' )[ 0 ] + '.' + "pdf"
		if ( filetype == "excel" ):
			self.frame_1 = ttk.Frame( master )
			self.message_1 = tk.Message( self.frame_1 )
			self.message_1.config(
			    background='#ffffff',
			    font='{Arial} 10 {bold}',
			    relief='flat',
			    text='Enter Sheet Number (,) seperated.\nEx. 1,2,3',
			    width='250'
			    )
			self.message_1.pack( side='top' )
			self.sheet_E = ttk.Entry( self.frame_1 )
			self.sheet_E.config( font='{Arial} 12 {bold}', takefocus=True, width='25' )
			self.sheet_E.pack( side='top' )
			self.conert_B = ttk.Button( self.frame_1 )
			self.conert_B.config( default='normal', state='normal', takefocus=True, text='Convert' )
			self.conert_B.pack( side='top' )
			self.conert_B.configure( command=self.exceltopdf )
			self.frame_1.config( height='200', width='200' )
			self.frame_1.pack( side='top' )
			self.sheet_E.focus_set()
			self.frame_1.place( anchor='n', relx='0.5', rely='0.1', x='0', y='0' )
			# Main widget
			self.mainwindow = self.frame_1

		elif ( filetype == "word" ):
			self.doctopdf()

		pass

	def doctopdf( self ):
		self.dir = filedialog.askdirectory( title="Select Directory" )
		self.outpath = os.path.join( self.dir, self.filename )
		print( self.outpath )
		if ( self.dir == "" ):
			messagebox.showerror( "Invadid", "Invalid Directory !" )
		else:
			try:
				word = client.DispatchEx( 'Word.Application' )
				doc = word.Documents.Open( self.filepath )
				tp = os.path.join( tempfile.gettempdir(), self.filename )
				doc.SaveAs( tp, FileFormat=17 )
				shutil.copy2( tp, self.outpath )
				os.remove( tp )
				messagebox.showinfo( "Done", "Converted !" )
			except Exception as e:
				messagebox.showerror( "Error", "Something Went Wrong !" )
				print( e )
			finally:
				doc.Close()
				word.Quit()

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

	def exceltopdf( self, sheets=[ 1 ] ):
		self.sheets = self.sheet_E.get()
		self.frame_1.destroy()
		self.dir = filedialog.askdirectory( title="Select Directory" )
		self.outpath = os.path.join( self.dir, self.filename )
		if os.path.exists( self.outpath ):
			os.remove( self.outpath )
		try:
			sheets = [ int( x ) for x in self.sheets.split( ',' ) ]
		except:
			messagebox.showerror( "error", "Enter Sheet Number (,) seperated.\nDefault is 1" )
			sheets = [ 1 ]

		if ( self.dir == "" ):
			messagebox.showerror( "Invadid", "Invalid Directory !" )
		else:

			try:
				excel = client.DispatchEx( "Excel.Application" )
				tp = os.path.join( tempfile.gettempdir(), self.filename )
				wb = excel.Workbooks.Open( self.filepath )
				wb.Worksheets( sheets ).Select()
				wb.SaveAs( tp, FileFormat=57 )
				shutil.copy2( tp, self.outpath )
				os.remove( tp )
				messagebox.showinfo( "Done", "Converted !" )

			except Exception as e:
				print( e )
				messagebox.showerror( "Error", "Something Went Wrong !" )
			finally:
				wb.Close()
				excel.Quit()

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

	def run( self ):
		self.mainwindow.mainloop()


# c = Convert2pdf()
# c.exceltopdf()
if __name__ == '__main__':
	root = tk.Tk()
	app = Convert2pdf( 'excel', root )
	app.run()
