import os
import tkinter
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import markdown
from pdfkit import from_string

class MarkdownEngine:

	root = Tk()
	width = 600
	height = 400
	savename = None

	def __init__(self):

		self.root.title("Untitled")
		self.TextArea = Text(self.root)
		self.scrollbar = Scrollbar(self.TextArea)
		self.menubar = Menu(self.root)
		self.help_menu = Menu(self.menubar)
		self.menufile = Menu(self.menubar)
		self.menuconv = Menu(self.menubar)




		screenWidth = self.root.winfo_screenwidth()
		screenHeight = self.root.winfo_screenheight()
	
		left = (screenWidth / 2) - (self.width / 2)
		top = (screenHeight / 2) - (self.height /2)
		
		self.root.geometry(f'{self.width}x{self.height}+{int(left)}+{int(top)}')
		self.root.grid_rowconfigure(0, weight=1)
		self.root.grid_columnconfigure(0, weight=1)
		self.TextArea.grid(sticky = N + E + S + W)
		self.menufile.add_command(label="Open",command=self.openfile)
		self.menufile.add_command(label="New",command=self.new)
		self.menufile.add_command(label="Save",command=self.saveFile)
		self.menufile.add_command(label="Exit",command=self.quitApp)		

		self.menufile.add_separator()
		self.menuconv.add_command(label="pdf",command=self.toPdf)			
		self.menuconv.add_command(label="html",command=self.toHtml)
		# self.menuconv.add_command(label="LateX",command=self.toLatex)			

		self.help_menu.add_command(label="About MarkdownEngine",command=self.about)
		self.help_menu.add_command(label="Shortcuts",command=self.keyBsh)

		
		# update menubar
		self.menubar.add_cascade(label="File",menu=self.menufile)	
		self.menubar.add_cascade(label="Help",menu=self.help_menu)
		self.menubar.add_cascade(label="convert", menu=self.menuconv)
		self.root.config(menu=self.menubar)
		self.scrollbar.pack(side=RIGHT,fill=Y)				
		self.scrollbar.config(command=self.TextArea.yview)	
		self.TextArea.config(yscrollcommand=self.scrollbar.set)
		# keyboard shortcut 
		self.root.bind('<Control-n>', lambda newfile : self.new())
		self.root.bind('<Control-o>', lambda open : self.openfile())
		self.root.bind('<Control-s>', lambda save : self.saveFile())
		self.root.bind('<Control-x>', lambda save : self.quitApp())
		# convert to pdf
		self.root.bind('<Control-p>', lambda save : self.toPdf())
		# convert to html
		self.root.bind('<Control-h>', lambda save : self.toHtml())




	
		
	def quitApp(self):
		self.root.destroy()

	def about(self):
		txt = """
			MarkdownEngine is a notepad that alows you to write markdown
			and convert to pdf or html. It is developed by Chris Byron
		"""
		showinfo("MarkdownEngine",txt)

	def keyBsh(self):
		txt = """
			ctrl + n - new file
			ctrl + o - open file
			ctrl + s - save file
			ctrl + p - convert to pdf
			ctrl + h - convert to html
			ctrl + x - close
				"""
		showinfo("MarkdownEngine keyboard Shortcuts", txt)

	def openfile(self):
		
		self.savename = askopenfilename(filetypes=(("Markdown File", "*.md , *.mdown , *.markdown"),
                                                            ("Text File", "*.txt"),
                                                            ("All Files", "*.*")))

		if not self.savename:			
			self.savename = None
		else:
			
			self.root.title(os.path.basename(self.savename) + " - MarkdownEngine")
			self.TextArea.delete(1.0,END)

			file = open(self.savename,"r")

			self.TextArea.insert(1.0,file.read())

			file.close()

	def toPdf(self):
		if self.savename == None or not self.savename:
			self.saveFile()
		try:	
			pre, ext = os.path.splitext(self.savename)
			pfile = pre + ".pdf" 
			file = open(self.savename,"w")
			filec = markdown.markdown(self.TextArea.get(1.0,END))
			file.write(filec)
			from_string(filec, pfile)
		except TypeError as e:
			pass
			

	def toHtml(self):
		if self.savename == None or not self.savename:
			self.saveFile()
		try:	
			pre, ext = os.path.splitext(self.savename)
			pfile = pre + ".html" 
			file = open(pfile,"w")
			filec = markdown.markdown(self.TextArea.get(1.0,END))
			file.write(filec)
			file.close()
		except TypeError as e:
			pass 		

		
	def new(self):
		self.root.title("Untitled - MarkdownEngine")
		self.savename = None
		self.TextArea.delete(1.0,END)


	def saveFile(self):

		if self.savename == None:
			# Save  file
			self.savename = asksaveasfilename(initialfile='Untitled.md',
											defaultextension=".md",
											filetypes=[("All Files","*.*"),
												("Text Documents","*.txt"), 
												("Markdown File", "*.md , *.mdown , *.markdown")])

			if not self.savename:
				self.savename = None
			else:
				
				# save file
				
				file = open(self.savename,"w")
				file.write(self.TextArea.get(1.0,END))
				file.close()
				
				# Change title
				self.root.title(os.path.basename(self.savename) + " - MarkdownEngine")
				
			
		else:
			file = open(self.savename,"w")
			file.write(self.TextArea.get(1.0,END))
			file.close()


	def run(self):
		self.root.mainloop()




markd = MarkdownEngine()
markd.run()
