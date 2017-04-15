import numpy as np
from scipy.sparse import coo_matrix

indd =  {
    'chinese.json_3.txt': ['chinese', 'macao'],
    'chinese.json_1.txt': ['chinese', 'beijing', 'chinese'],
    'chinese.json_2.txt': ['chinese', 'chinese', 'shanghai'],
    'japanese.json_1.txt': ['tokyo', 'japan', 'chinese']
}


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
print dtm.toarray()

