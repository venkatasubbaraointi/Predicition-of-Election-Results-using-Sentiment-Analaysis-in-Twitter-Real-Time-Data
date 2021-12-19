#preprocessing
import csv
import re
import string
from nltk.corpus import stopwords

tweet=[]
input=open("result.csv","r")
output=open("sample_result.csv","w")
reader=csv.reader(input)
writer=csv.writer(output,delimiter='\n',quoting=csv.QUOTE_NONE,escapechar=' ')
stop_words=set(stopwords.words('english'))   #importing stopwords related to english

for row in reader:
	rrow=''.join(row[1])
	rrow=rrow.lower()   	#converting into lowercase

	rrow=rrow.translate(rrow.maketrans("","","~_=+><*.,/';:?-!%"))   #removing special characters
	rrow=re.sub(r'[0-9]+',"", rrow)   #removing words containing numericals

	words=rrow.split()
	cword=[]
	for word in words:
		if 'rt' not in word and '@' not in word and '#' not in word and 'http' not in word and '\\x' not in word:
			if(word not in stop_words):
				cword.append(word)		#removing hashtags and stopwords
	tweet.append(' '.join(cword))

writer.writerow(tweet)		#appending to new file
input.close()
output.close()

