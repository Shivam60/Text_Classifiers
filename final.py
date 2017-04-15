import scipy.io
from scipy.sparse import coo_matrix
import json,os,time
if __name__ == '__main__':
	train_js={}
	dt=scipy.io.mmread(os.getcwd()+r'/input/jsons/'+"dtm") #loading matrix
	dtm=dt.toarray()
	#loading trained values
	try:
		with open(os.getcwd()+r'/input/jsons/'+"trained",'r') as file1:
			dp=file1.read()
			file1.close()
		train_js=json.loads(dp)
	except IOError as err:
		print err
	cat_list=train_js['cat_list']
	cat_prob=train_js['cat_prob']
	cat_list_value=train_js['cat_list_value']
	vocab_value=train_js['vocab_value']
	voc=train_js['vocab']
	sent="Chinese Chinese Chinese Tokyo Japan".split()
	print cat_list_value
	for i in xrange(len(sent)):
		sent[i]=sent[i].lower()
	for key in cat_prob: #for a particluar category
		cat=key #find the category name
		cat_present_doc=cat_list_value[cat] #find the docs present in the categories
		for word in sent: #for each word
			word_freq_class=0
			vocab_val=vocab_value[word] #find the index of each word in our vocab 
			for i in xrange(len(cat_present_doc)):
				word_freq_class+=dtm[cat_present_doc[i],vocab_val]
			word_freq_class+=1
			print word, cat, word_freq_class

