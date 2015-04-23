import pprint
import pylab as pl

def ShowBarPlots(location,standard,data,name):
	st = []
	val = standard
	for i in range(7):
		st.append(val)
	fig = pl.figure(name)
	line = pl.plot(range(7),st,color='red')
	ax = fig.add_subplot(111)
	ax.bar([1.5,2.5,3.5,4.5], data,color='black',width=0.5)
	ax.set_xlim(1,5.75)
	ax.set_ylabel(name)
	ax.set_title('{0} in Delhi'.format(name))
	xTickMarks = [i for i in location]
	ax.set_xticks([1.7,2.7,3.7,4.7])
	xtickNames = ax.set_xticklabels(xTickMarks)
	pl.setp(xtickNames)
	pl.legend(line,("Standard",),loc='best')
	pl.show()


def ShowData(data): #add data feild
	location = []
	for key in data['location']:
		location.append(key)
	ozone = []
	p10 = []
	p2 = []
	for l in location:
		ozone.append(data['location'][l]['ozone'])
		p10.append(data['location'][l]['particulate10'])
		p2.append(data['location'][l]['particulate2'])
	for i in range(len(ozone)):
		if ozone[i]==None:
			ozone[i] = 0
	for i in range(len(p10)):
		if p10[i]==60:
			p10[i] = 0
	for i in range(len(p2)):
		if p2[i]==100:
			p2[i] = 0
	try:
		if None not in ozone:
			ShowBarPlots(location,data['standard']['ozone'],ozone,"ozone")
	except:
		print "Data Insufficient for Ozone."
	ShowBarPlots(location,data['standard']['particulate10'],p10,"particulate10")
	ShowBarPlots(location,data['standard']['particulate2'],p2,"particulate2")


