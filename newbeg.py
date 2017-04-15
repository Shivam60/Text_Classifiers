import json,os,time
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import numpy as np
import scipy.io
from scipy.sparse import coo_matrix
if __name__ == '__main__':
    start=time.time()
    print "Program started at: ",start
   # processes_limit=int(sys.argv[1])
   # threads=int(sys.argv[2])
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
    train_js['vocab_value']=vocab_value    
    train_js['cat_list']=cat_list
    train_js['cat_prob']=cat_prob
    train_js['cat_list_value']=cat_list_value
    with open(os.getcwd()+r'/input/jsons/'+"trained",'w') as file1:
    	dp=json.dumps(train_js, sort_keys=True, indent=4, separators=(',', ': '))
    	file1.write(dp)
    	file1.close()
    scipy.io.mmwrite(os.getcwd()+r'/input/jsons/'+"dtm",dtm)
    print train_js
    end=time.time()
    print "Program ended at: ",end
    print "Total Time to process: ",end-start
