#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from Tkinter import *
from Analysis.Analysis import *

class Gui(object):                         
	def __init__(self, myParent):
		if len(sys.argv)>1 and sys.argv[1] in ["CMD",'cmd','cl']:
			self.Cmdline()
			sys.exit()     
		self.myContainer = Frame(myParent,height=200,width=200)
		self.myContainer.pack()

		Label(self.myContainer, text="Choose an Element:").pack(anchor=W)
		self.v = StringVar()
		element = [
    					(u"Ozone \u03bcg/m\xb3",'oz'),
    					(u"Particulate < 10 \u03bcg/m\xb3",'p10'),
    					(u"Particulate < 2.5 \u03bcg/m\xb3",'p2'),
					]
		for txt,val in element:
			Radiobutton(self.myContainer, 
                text=txt,
                indicatoron = 0,
                width = 64,
                padx = 20, 
                variable=self.v, 
                command=self.showText,
                value=val).pack(anchor=W)

		self.var1 = StringVar()
		self.C1 = Checkbutton(self.myContainer, text="Anand Vihar ",variable = self.var1,onvalue="AV",offvalue="")
		self.var2 = StringVar()
		self.C2 = Checkbutton(self.myContainer, text="Mandir Marg ",variable = self.var2,onvalue="MM",offvalue="")
		self.var3 = StringVar()
		self.C3 = Checkbutton(self.myContainer, text="Punjabi Bagh",variable = self.var3,onvalue="PB",offvalue="")
		self.var4 = StringVar()
		self.C4 = Checkbutton(self.myContainer, text="R.K Puram  ",variable = self.var4,onvalue="RKP",offvalue="")
	
		self.button1 = Button(self.myContainer,command=self.combine) 
		self.button1["text"]= "Execute"           
		Label(self.myContainer, text="\nChoose Location(s):").pack(anchor = W)
		self.C1.pack(anchor=W)
		self.C2.pack(anchor=W)
		self.C3.pack(anchor=W)
		self.C4.pack(anchor=W)
		#Label(self.myContainer, text="\n").pack() 
		self.button1.pack()	
		self.text = None
		self.ozone = None
		self.particulate = None
		with open('ozone.txt','r') as f:
			self.ozone = f.read()

		with open('particulate.txt','r') as f:
			self.particulate = f.read()
	
	def combine(self):
		self.buildCmd()
		try:
			self.forget()
		except:
			return

	def forget(self):
		self.text.destroy()
		self.text = None

	def showText(self):
		"""After selecting an element have to select location(s)"""
		if	self.v.get()=="oz" and self.text==None:
			self.text = Text(self.myContainer,width=67, height=25)
			self.text.configure(state='normal')
			self.text.insert('1.0', self.ozone)
			self.text.configure(state='disabled')
			self.text.pack()
		elif (self.v.get()=="p2" or self.v.get()=="p10") and self.text==None:
			self.text = Text(self.myContainer,width=67, height=25)
			self.text.configure(state='normal')
			self.text.insert('1.0', self.particulate)
			self.text.configure(state='disabled')
			self.text.pack()
		

	def buildCmd(self):
	   		
	   	s = "get %s in %s %s %s %s till now" % (self.v.get(),self.var1.get(), self.var2.get(),self.var3.get(),self.var4.get())
	   	query = s.split()
	   	if len(query)<6 or query[1]=='in': #Need to check for locations missing
			return
	   	if query[0]=='get':
			get_data(query[1:])
	
	def Cmdline(self):
		#q = {"date":datetime(2015,04,23,15,10)}
		#find_data(q)[0]
		while True:
			print ""
			print "Elements = oz: ozone , p10: particulate < 10 , p2: particulate < 2.5"
			print "Location = RK: RK Puram , MM: Mandir Marg , AV: Anand Vihar, PB: Punjabi Bagh"
			print "Quit = q"
			print "Enter Query:",
			try:
				s = raw_input()
				if s in ["quit","q",'exit']:
					break
				query = s.split()
			
				if query[0]=='get':
					check = get_data(query[1:])
					if check==0:
						print "Error in Query"
						continue
			except:
				continue
		print "Bye" 


if __name__ == '__main__':
		root = Tk()
		root.title("Pollution Analysis")
		myapp = Gui(root)
		root.mainloop()     