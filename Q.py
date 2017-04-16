import scipy.io
from scipy.sparse import coo_matrix
import json,os,time,math,operator,enchant,string,time,os
import numpy as np
from nltk.corpus import stopwords
words=enchant.Dict("en_US")
stop = stopwords.words('english') + list(string.punctuation)

def preprocess_text(arg):
	arg=[k for k in arg if k.isalnum() or k==" " or k=="\n"]
	arg=[word for word in arg if word not in stop and words.check(word)]
	arg=[k.lower() for k in arg]
	arg=[k for k in arg if k in voc]
	return arg
if __name__ == '__main__':
    start=time.time()
    #processes_limit=int(sys.argv[1])
    #threads=int(sys.argv[2])
    processes_limit=3
    threads=30
    print "Program started at: ",start
    #print "Number of Processors used: ", processes_limit
    #print "Number of Threads used: ", threads
    cwd=os.getcwd()
    train=cwd+r"/input/train/"
    categories=os.listdir(train)
    train_js={}
    dt=scipy.io.mmread(os.getcwd()+r'/input/jsons/'+"dtm") #loading matrix
    dtm=dt.toarray()
    with open(os.getcwd()+r'/input/jsons/'+"trained",'r') as file1:
		  dp=file1.read()
		  file1.close()
    train_js=json.loads(dp)
    cat_list=train_js['cat_list']
    cat_prob=train_js['cat_prob']
    proab={}
    for i in cat_prob:
        proab[i]=0.0
    cat_list_value=train_js['cat_list_value']
    vocab_value=train_js['vocab_value']
    voc=train_js['vocab']
    with open("test.txt",'r') as file1:
        sent=file1.read()
        file1.close()
    sent=preprocess_text(sent.split())
    for key in cat_prob: #for a particluar category
		cat=key #find the category name
		cat_present_doc=cat_list_value[cat]
		no=0 #find the docs present in the categories
		for word in sent: #for each word
			words_in_class=0 #to find the vocab of a class
			word_freq_class=0
			print cat," ",word," ",no
			no+=1
			vocab_val=vocab_value[word] #find the index of each word in our vocab 
			for i in xrange(len(cat_present_doc)):
				word_freq_class+=dtm[cat_present_doc[i],vocab_val]
				words_in_class+=np.sum(dtm[cat_present_doc[i]])
			word_freq_class+=1			
			proab[cat]+=math.log(float(word_freq_class)/(float(words_in_class)+len(voc))) #to calculate the probablity by computing its log instead and adding 
		proab[cat]+=math.log(float(cat_prob[cat]))#adding naives posterior probablity of the categor
sorted_proab = sorted(proab.items(), key=operator.itemgetter(1)) #sorting the dicitionary by values in ascending value
print(sorted_proab)
print(sorted_proab[len(sorted_proab)-1][0])
