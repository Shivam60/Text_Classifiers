import pandas as pd
import os,json

with open(os.getcwd()+r'/input/jsons/'+r'vocap.json','r') as file1:
    vocab=file1.read()
file1.close()

vocab=json.loads(vocab)
ds={}
preprob={}
preprobn={}
s=pd.read_csv(os.getcwd()+r'/input/jsons/docmat.csv')

ls=[]
for index,row in s.iterrows():
    ds[row['categories_of_docs']]=0
    ls.append(row['categories_of_docs'])
for cat in ls:
    ds[cat]+=1.0
for cat in ds:
    ds[cat]=ds[cat]/len(ls)

for i in ds:
     q=pd.DataFrame(s[(s['categories_of_docs'])==str(i)]).sum(0)
     q=q[1:len(vocab)+1:]
     doclen=q.sum(0)
     q=q+1
     q=q/(len(vocab)+doclen)
     preprob[i]=q
     preprobn[i]=json.loads(q.to_json())

with open(os.getcwd()+r'/input/jsons/'+r'trained_val.json','w') as file1:
    dp=json.dumps(preprobn, sort_keys=True, indent=4, separators=(',', ': '))
    file1.write(dp)
file1.close()

