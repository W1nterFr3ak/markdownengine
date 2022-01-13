import os
import tkinter as tk
import tkinter.filedialog as diag
import tkinter.messagebox as mbox
from time import sleep
import markdown
from pdfkit import from_string
from tkhtmlview import HTMLLabel

class MarkdownEngine:

	root = tk.Tk()
	width = 600
	height = 400
	savename = None

	def __init__(self):

		self.root.title("Untitled")
		self.TextArea = tk.Text(self.root)
		self.scrollbar = tk.Scrollbar(self.TextArea)
		self.menubar = tk.Menu(self.root)
		self.help_menu = tk.Menu(self.menubar)
		self.menufile = tk.Menu(self.menubar)
		self.menuconv = tk.Menu(self.menubar)




		screenWidth = self.root.winfo_screenwidth()
		screenHeight = self.root.winfo_screenheight()
	
		left = (screenWidth / 2) - (self.width / 2)
		top = (screenHeight / 2) - (self.height /2)
		
		self.root.geometry(f'{self.width}x{self.height}+{int(left)}+{int(top)}')
		# self.root.grid_rowconfigure(0, weight=1)
		# self.root.grid_columnconfigure(0, weight=1)
		# self.TextArea.grid(sticky = tk.N + tk.E + tk.S + tk.W)

		# self.root.pack(fill=tk.BOTH, expand=1)
		self.TextArea = tk.Text(self.root, width="1")
		self.TextArea.pack(fill=tk.BOTH, expand=1, side=tk.LEFT)
		self.outputTextArea = HTMLLabel(
		self.root, width="1", background="white", html="<h1>MarkdownEngine Preview Pane</h1>")
		self.outputTextArea.pack(fill=tk.BOTH, expand=1, side=tk.RIGHT)
		self.outputTextArea.fit_height()
		self.TextArea.bind("<<Modified>>", self.priv)

		self.menufile.add_command(label="Open",command=self.openfile)
		self.menufile.add_command(label="New",command=self.new)
		self.menufile.add_command(label="Save",command=self.saveFile)
		self.menufile.add_command(label="Exit",command=self.quitApp)		

		self.menufile.add_separator()
		self.menuconv.add_command(label="pdf",command=self.toPdf)			
		self.menuconv.add_command(label="html",command=self.toHtml)
		# self.menuconv.add_command(label="LateX",command=self.toLatex)
		# self.menuconv.add_command(label='preview', command=self.priv)		

		self.help_menu.add_command(label="About MarkdownEngine",command=self.about)
		self.help_menu.add_command(label="Shortcuts",command=self.keyBsh)

		
		# update menubar
		self.menubar.add_cascade(label="File",menu=self.menufile)	
		self.menubar.add_cascade(label="Help",menu=self.help_menu)
		self.menubar.add_cascade(label="convert", menu=self.menuconv)

		self.root.config(menu=self.menubar)
		self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)				
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
		mbox.showinfo("MarkdownEngine",txt)
	# def priv(self):
	# 	rd = markdown.markdown(self.TextArea.get(1.0,tk.END))
	# 	mbox.showinfo('preview',rd)

	def priv(self, event):
		self.TextArea.edit_modified(0)
		md2html = markdown.Markdown()
		markdownText = self.TextArea.get("1.0", tk.END)
		html = md2html.convert(markdownText)
		self.outputTextArea.set_html(html)

	def keyBsh(self):
		txt = """
			ctrl + n - new file
			ctrl + o - open file
			ctrl + s - save file
			ctrl + p - convert to pdf
			ctrl + h - convert to html
			ctrl + x - close
				"""
		mbox.showinfo("MarkdownEngine keyboard Shortcuts", txt)

	def openfile(self):
		
		self.savename = diag.askopenfilename(filetypes=(("Markdown File", "*.md , *.mdown , *.markdown"),
                                                            ("tk.Text File", "*.txt"),
                                                            ("All Files", "*.*")))

		if not self.savename:			
			self.savename = None
		else:
			
			self.root.title(os.path.basename(self.savename) + " - MarkdownEngine")
			self.TextArea.delete(1.0,tk.END)

			file = open(self.savename,"r")
			print(f"[+] File : {self.savename} Opened Succesfull")


			self.TextArea.insert(1.0,file.read())

			file.close()

	def toPdf(self):
		if self.savename == None or not self.savename:
			self.saveFile()
		try:	
			pre, ext = os.path.splitext(self.savename)
			pfile = pre + ".pdf" 
			filec = markdown.markdown(self.TextArea.get(1.0,tk.END))
			try:
				from_string(filec, pfile)
				print("[+] Pdf conversion Succesfull")
			except OSError:
				print(f"[!] Normal conversion failed: copying content directly to {pfile}")
				file = open(pfile, 'w')
				file.write(filec)
				sleep(3)
				print("[!] Cleaning : Note pdf my contain errors")
				sleep(2)
				print("[!] Info : Check if the static files linked in the markdown are availabel")
				sleep(2)
				print("[!] Use absolute refrence")
				sleep(2)
				print("[+] Bytes copied Succesfully")
				file.close()


		except TypeError as e:
			print("[!] Pdf conversion Failed")
			pass
			

	def toHtml(self):
		if self.savename == None or not self.savename:
			self.saveFile()
		try:	
			pre, ext = os.path.splitext(self.savename)
			print(pre)
			pfile = pre + ".html" 
			file = open(pfile,"w")
			filec = markdown.markdown(self.TextArea.get(1.0,tk.END))
			file.write(filec)
			file.close()
			print("[+] Html conversion Succesfull")
		except TypeError as e:
			print("[!] Html conversion failed")
			pass 		

		
	def new(self):
		self.root.title("Untitled - MarkdownEngine")
		self.savename = None
		self.TextArea.delete(1.0,tk.END)


	def saveFile(self):

		if self.savename == None:
			# Save  file
			self.savename = diag.asksaveasfilename(initialfile='Untitled.md',
											defaultextension=".md",
											filetypes=[("All Files","*.*"),
												("tk.Text Documents","*.txt"), 
												("Markdown File", "*.md , *.mdown , *.markdown")])

			if not self.savename:
				self.savename = None
			else:
				
				# save file
				
				file = open(self.savename,"w")
				file.write(self.TextArea.get(1.0,tk.END))
				file.close()
				print(f"[+] File : {self.savename} Creation Succesfull")

				
				# Change title
				self.root.title(os.path.basename(self.savename) + " - MarkdownEngine")
				
			
		else:
			file = open(self.savename,"w")
			file.write(self.TextArea.get(1.0,tk.END))
			file.close()
			print(f"[+] File : {self.savename} Saving Succesfull")



	def run(self):
		self.root.mainloop()




markd = MarkdownEngine()
markd.run()
