#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from Tkinter import *
from Analysis import *

class MyApp(object):                         
	def __init__(self, myParent):     
		self.myContainer = Frame(myParent,height=200,width=200)
		self.myContainer.pack()

		Label(self.myContainer, text="Choose an Element:\n").pack()
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
                width = 20,
                padx = 20, 
                variable=self.v, 
                command=None,
                value=val).pack(anchor=W)
		
		self.var1 = StringVar()
		self.C1 = Checkbutton(self.myContainer, text="Anand Vihar ",variable = self.var1,onvalue="AV",offvalue="")
		self.var2 = StringVar()
		self.C2 = Checkbutton(self.myContainer, text="Mandir Marg ",variable = self.var2,onvalue="MM",offvalue="")
		self.var3 = StringVar()
		self.C3 = Checkbutton(self.myContainer, text="Punjabi Bagh",variable = self.var3,onvalue="PB",offvalue="")
		self.var4 = StringVar()
		self.C4 = Checkbutton(self.myContainer, text="R.K Puram  ",variable = self.var4,onvalue="RKP",offvalue="")
	
		self.button1 = Button(self.myContainer,command=self.buildCmd) 
		self.button1["text"]= "Execute"           
		Label(self.myContainer, text="\nChoose Location(s):").pack()
		self.C1.pack()
		self.C2.pack()
		self.C3.pack()
		self.C4.pack()
		Label(self.myContainer, text="\n").pack() 
		self.button1.pack()	
	
	def buildCmd(self):
   		s = "get %s in %s %s %s %s till now" % (self.v.get(),self.var1.get(), self.var2.get(),self.var3.get(),self.var4.get())
   		query = s.split()
   		print query
   		if query[0]=='get':
			get_data(query[1:])
 

if __name__ == '__main__':
	if len(sys.argv)>1 and sys.argv[1] in ["CMD",'cmd','cl']:
		Cmdline()
	else:
		root = Tk()
		root.title("Pollution Analysis")
		myapp = MyApp(root)
		root.mainloop()     