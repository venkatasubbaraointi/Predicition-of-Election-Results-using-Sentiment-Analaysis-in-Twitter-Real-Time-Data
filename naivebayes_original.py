#vader sentiment analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
import matplotlib.pyplot as plt
import tkinter
import pandas as pd

input=open("sample_result.csv","r")
output=open("postrainedresults.csv","w")
output1=open("negtrainedresults.csv","w")
reader=csv.reader(input)
writer=csv.writer(output,delimiter='\n',quoting=csv.QUOTE_NONE,escapechar=' ')
writer1=csv.writer(output1,delimiter='\n',quoting=csv.QUOTE_NONE,escapechar=' ')
pos=0
neg=0
neu=0
postweet=[]
negtweet=[]

#main code for vader
analyser = SentimentIntensityAnalyzer()
def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    return score['compound']

for row in reader:
	val=sentiment_analyzer_scores(''.join(row))
	if val==0.0:
		neu=neu+1
	else:
		if val>0:
			pos=pos+1
			postweet.append(''.join(row))
		else:
			neg=neg+1
			negtweet.append(''.join(row))

writer.writerow(postweet)
writer1.writerow(negtweet)

#naaive bayes calculation

pofpos=pos/(pos+neg)
pofneg=neg/(pos+neg)
sum=0
totposwords=0
totnegwords=0
totwords=0
poslist=[]
neglist=[]
#counting total positive and negative words
for val in postweet:
	totposwords=totposwords+len(''.join(val).split())
	poslist.append(''.join(val).split())

for val in negtweet:
	totnegwords=totnegwords+len(''.join(val).split())
	neglist.append(''.join(val).split())

totwords=totposwords+totnegwords

def positiveprobability(readertest):
	count=[]
	posresults=[]
	for testrow in readertest:
		k=(''.join(testrow).split())
		for m in range(len(k)):
			ecount=0
			for n in range(len(poslist)):
				for l in range(len(poslist[n])):
					if(k[m]== poslist[n][l]):
						ecount=ecount+1
			count.append(ecount)
		prod=naive_bayes_pos(testrow,count)
		posresults.append(prod)
	return posresults

def negativeprobability(readertest1):
	count1=[]
	negresults=[]
	for testrow in readertest1:
		k=(''.join(testrow).split())
		for m in range(len(k)):
			ecount=0
			for n in range(len(neglist)):
				for l in range(len(neglist[n])):
					if(k[m]== neglist[n][l]):
						ecount=ecount+1
			count1.append(ecount)
		prod1=naive_bayes_neg(testrow,count1)
		negresults.append(prod1)
	return negresults

#calculating the probabilities
def naive_bayes_pos(testrow,count):
	prod=1
	for a in range(len(count)):
		ans=(count[a]+1)/(totwords+totposwords)
		prod=prod*ans
	return prod*pofpos

def naive_bayes_neg(testrow,count1):
	prod1=1
	for a in range(len(count1)):
		ans=(count1[a]+1)/(totwords+totnegwords)
		prod1=prod1*ans
	return prod1*pofneg

def calulate_final_polarity(posresults,negresults):
	poscount=0
	negcount=0
	for s in range(len(posresults)):
		if(posresults[s]>negresults[s]):
			poscount=poscount+1
		else:
			negcount=negcount+1
	return poscount,negcount

def naive_bayes(k):
        inputtest=open(k,"r")
        readertest=csv.reader(inputtest)
        inputtest2=open(k,"r")
        readertest1=csv.reader(inputtest2)

        #searching the key word
        m=0
        count=[]
        count1=[]
        posresults=[]
        negresults=[]
        posresults=positiveprobability(readertest)
        negresults=negativeprobability(readertest1)
        p,s=calulate_final_polarity(posresults,negresults)
        return p,s

def plotting(z,k):
        df = pd.DataFrame({
            "party": ["JSN", "TDP", "YSRCP"],
            "pos": z,
            "neg": k
        })
        df.set_index("party",drop=True,inplace=True)
        df.plot.bar()
        plt.show()

j_pos,j_neg=naive_bayes("prep_janasena.csv")
t_pos,t_neg=naive_bayes("prep_tdp.csv")
y_pos,y_neg=naive_bayes("prep_ysrcp.csv")

z=[]
z.append(j_pos)
z.append(t_pos)
z.append(y_pos)
k=[]
k.append(j_neg)
k.append(t_neg)
k.append(y_neg)

plotting(z,k)
print(j_pos,j_neg)
print(t_pos,t_neg)
print(y_pos,y_neg)

