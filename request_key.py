import tkinter as tk
import tkinter.ttk as ttk


class Request_Key:

	def __init__( self, master=None ):
		# build ui
		self.root = master
		frame_1 = ttk.Frame( master )
		label_1 = ttk.Label( frame_1 )
		self.img_tentativesoftwarebackground766x766 = tk.PhotoImage(
		    file='images/tentative software background_766x766.png'
		    )
		label_1.config( image=self.img_tentativesoftwarebackground766x766 )
		label_1.place( anchor='n', x='0', y='0' )
		getkey_M = tk.Message( frame_1 )
		getkey_M.config(
		    font='{Arial} 15 {bold}',
		    takefocus=False,
		    text='You Do not have a License Key.\nEnter Your Name.',
		    width='350'
		    )
		getkey_M.place( anchor='n', relx='0.5', rely='0.42', x='0', y='0' )
		name_E = ttk.Entry( frame_1 )
		name_E.config( font='{Arial} 12 {}', takefocus=True, width='31' )
		name_E.place( anchor='n', relx='0.5', rely='0.52', x='0', y='0' )
		getkey_B = ttk.Button( frame_1 )
		getkey_B.config( text='Get Key' )
		getkey_B.place( anchor='n', relx='0.5', rely='0.57', x='0', y='0' )
		frame_1.config( height='768', width='768' )
		frame_1.pack( anchor='center', expand='true', fill='y', side='top' )
		frame_1.pack_propagate( 0 )

		# Main widget
		self.mainwindow = frame_1

	def run( self ):
		self.mainwindow.mainloop()


if __name__ == '__main__':
	root = tk.Tk()
	app = Request_Key( root )
	app.run()
