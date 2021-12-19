#importing afinn dictionary from python libraries
import csv
import pandas as pd
import matplotlib.pyplot as plt
import tkinter
from afinn import Afinn

input=open("prep_janasena.csv","r")
input1=open("prep_tdp.csv","r")
input2=open("prep_ysrcp.csv","r")
reader=csv.reader(input)
reader1=csv.reader(input1)
reader2=csv.reader(input2)

af=Afinn()
#main code for afinn
def calculate_polarity(reader):
	pos=0
	neg=0
	neu=0
	postweet=[]
	negtweet=[]
	neutweet=[]
	for row in reader:
		val=af.score(''.join(row))
		if val==0.0:
			neu=neu+1
			neutweet.append(''.join(row))
		else:
			if val>0:
				pos=pos+1
				postweet.append(''.join(row))
			else:
				neg=neg+1
				negtweet.append(''.join(row))
	return pos,neg,neu

def plotting(z,k,l):
	df = pd.DataFrame({
	    "party": ["JSN", "TDP", "YSRCP"],
	    "pos": z,
	    "neg": k,
	    "neu": l
	})
	df.set_index("party",drop=True,inplace=True)
	df.plot.bar()
	plt.show()

j_pos,j_neg,j_neu=calculate_polarity(reader)
t_pos,t_neg,t_neu=calculate_polarity(reader1)
y_pos,y_neg,y_neu=calculate_polarity(reader2)

z=[]
z.append(j_pos)
z.append(t_pos)
z.append(y_pos)
k=[]
k.append(j_neg)
k.append(t_neg)
k.append(y_neg)
l=[]
l.append(j_neu)
l.append(t_neu)
l.append(y_neu)
print(z,k,l)
plotting(z,k,l)
