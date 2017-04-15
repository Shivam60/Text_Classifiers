import os,string,json,time,multiprocessing,enchant,sys
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from multiprocessing import Pool
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool
import numpy as np
import scipy.io
from scipy.sparse import coo_matrix
words=enchant.Dict("en_US")
stop = stopwords.words('english') + list(string.punctuation)
def vocap_category(arg):
	folder_name=arg[0].split("/")
	doc=set()
	folder_name=folder_name[len(folder_name)-2]
	with open(os.getcwd()+r'/input/jsons/'+str(folder_name)+r'.json','r') as file1:
		dp=file1.read()
		dp=json.loads(dp)
		for i in dp:
			for sub in dp[i]:
				doc=doc.union(set( dp[i][sub].split()))
	return doc
def process_folder(arg):
    files=[]
    path=arg[0]
    threads=int(arg[1])
    folder_name=path.split('/')
    folder_name=folder_name[len(folder_name)-2]
    d={}
    for i in os.listdir(path):
        files.append([i,path+i])
    a={}
    d={}
    for i in files:
    	with open(i[1],'r') as file1:
    		doc=file1.read()
    		file1.close()    		
    	doc=" ".join([k for k in doc.split() if k.isalnum() or k==" " or k=="\n"])
    	doc=" ".join([word for word in doc.split() if word not in stop and words.check(word)])
    	doc=" ".join([k.lower() for k in doc.split()])		
    	d[str(i[0])]=doc
    a[folder_name]=d	    
    #print folder_name,len(a[folder_name]),"files Indexed"
    with open(os.getcwd()+r'/input/jsons/'+str(folder_name)+r'.json','w') as file1:
        dp=json.dumps(a, sort_keys=True, indent=4, separators=(',', ': '))
        file1.write(dp)
        file1.close()
    return 1
def join_JSON():
    bag={}
    json_files = [pos_json for pos_json in os.listdir(os.getcwd()+r'/input/jsons') if pos_json.endswith('.json')]
    for i in json_files:
        with open(os.getcwd()+r'/input/jsons/'+str(i),'r') as file1:
            dp=file1.read()
            dp2=json.loads(dp)
            for cat in dp2:
		print cat
	        bag[str(cat)]=dp2[cat]
            file1.close()
    with open(os.getcwd()+r'/input/jsons/train-multi.json','w') as file1:
        bag=json.dumps(bag, sort_keys=True, indent=4, separators=(',', ': '))
        file1.write(bag)

if __name__ == '__main__':
    start=time.time()
    #processes_limit=int(sys.argv[1])
    #threads=int(sys.argv[2])
    processes_limit=3
    threads=30
    print "Program started at: ",start
    print "Number of Processors used: ", processes_limit
    print "Number of Threads used: ", threads
    cwd=os.getcwd()
    train=cwd+r"/input/train/"
    categories=os.listdir(train)
    itter=[]
    for i in range(0,len(categories)):
        itter.append([train+categories[i]+r'/',threads])
    p = Pool(processes=processes_limit)
    results=p.map(process_folder, itter)
    #code to combine all jsons
    join_JSON()
    #code to make vocabulary
    p = Pool(processes=processes_limit)
    results=p.map(vocap_category, itter)
    voc=set()#set of all unique words in a dataset
    for i in results:
    	voc=voc.union(i)
    bag={}
    try:
        with open(r'/home/shivam/Programing/Current_Projects/Text_Classifiers/input/jsons/train-multi.json','r') as file1:
            dp=file1.read()    
            file1.close()
	    bag=json.loads(dp)
    except IOError as err:
        print err
    indd={}
    for cat in bag:
    	for sub in bag[cat]:
    		indd[str(cat)+"_"+str(sub)]=str(bag[cat][sub]).split()
    n_nonzero = 0
    vocab=set()
    for docterms in indd.values():
    	unique_terms = set(docterms)
    	vocab |= unique_terms
    	n_nonzero += len(unique_terms)
    docnames = list(indd.keys())
    docnames = np.array(docnames)
    vocab = np.array(list(vocab))
    vocab_sorter = np.argsort(vocab)
    ndocs = len(docnames)
    nvocab = len(vocab)
    data = np.empty(n_nonzero, dtype=np.intc)
    rows = np.empty(n_nonzero, dtype=np.intc)
    cols = np.empty(n_nonzero, dtype=np.intc)
    ind = 0
    for docname, terms in indd.items():
    	term_indices = vocab_sorter[np.searchsorted(vocab, terms, sorter=vocab_sorter)]
    	uniq_indices, counts = np.unique(term_indices, return_counts=True)
    	n_vals = len(uniq_indices)
    	ind_end = ind + n_vals
    	data[ind:ind_end] = counts
    	cols[ind:ind_end] = uniq_indices
    	doc_idx = np.where(docnames == docname)
    	rows[ind:ind_end] = np.repeat(doc_idx, n_vals)
    	ind = ind_end
    dtm = coo_matrix((data, (rows, cols)), shape=(ndocs, nvocab), dtype=np.intc)
    print dtm
    cat_list=[]
    cat_prob={}
    cat_list_value={} #a list of each category where the values indicate the particulat docs belonging to it
    vocab_value={} #for each vocab write the position  the occuring word
    for i in docnames: #all categories are arranged in the order of matrix representing each row's term frequencey count
    	n=i.split('_')
    	cat_list.append(n[0])
    	cat_prob[n[0]]=0.0  #for probablity of each category
    for i in xrange(len(cat_list)):
    	cat_prob[cat_list[i]]+=1.0
    	cat_list_value[cat_list[i]]=[]
    total_val=sum(cat_prob.values())
    for i in cat_prob:
    	cat_prob[i]=cat_prob[i]/total_val
    #for each vocab write the position  the occuring word
    for i in xrange(len(vocab)):
    	vocab_value[vocab[i]]=i
    #for each cat write the position of docs belonging to a category
    for i in xrange(len(cat_list)):
    	a=cat_list_value[cat_list[i]]
    	a.append(i)
    	cat_list_value[cat_list[i]]=a
    train_js={}
    train_js['vocab']=list(voc)
    print train_js['vocab']
    train_js['vocab_value']=vocab_value    
    train_js['cat_list']=cat_list
    train_js['cat_prob']=cat_prob
    train_js['cat_list_value']=cat_list_value
    with open(os.getcwd()+r'/input/jsons/'+"trained",'w') as file1:
    	dp=json.dumps(train_js, sort_keys=True, indent=4, separators=(',', ': '))
    	file1.write(dp)
    	file1.close()
    scipy.io.mmwrite(os.getcwd()+r'/input/jsons/'+"dtm",dtm)
    end=time.time()
    print "Program ended at: ",end
    print "Total Time to process: ",end-start
    end=time.time()
    print "Program ended at: ",end
    print "Total Time to process: ",end-start
    sys.exit(end-start)
