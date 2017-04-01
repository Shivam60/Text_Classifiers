import json,os
import pandas as pd

vocap=set()
fin={}
with open(os.getcwd()+r'/input/jsons/'+r'train.json','r') as file1:
    dp=file1.read()    
file1.close()
bag=json.loads(dp)
for categories in bag:
    for files in bag[categories]:
       vocap=vocap.union(set(" ".join(bag[categories][files]).split()))
vocap=list(vocap)
for i in range(len(vocap)):
    fin[i]=vocap[i]
s=pd.DataFrame(columns=vocap)
s['categories_of_docs']=0
cnt=0
for categories in bag:
    for subfile in bag[categories]:
        print "Processing File: ",subfile,"Number of Files Processed: ",cnt
        s.loc[str(subfile)]=0
        l1=" ".join(bag[categories][subfile]).split()
        for i in l1:
            s.loc[str(subfile),i]+=1  
        s.loc[str(subfile),'categories_of_docs']=str(categories)
        cnt+=1

for index,row in s.iterrows():
    print index,row['categories_of_docs']

s.to_csv(os.getcwd()+r'/input/jsons/docmat.csv')
with open(os.getcwd()+r'/input/jsons/vocap.json','w') as file1:
    dp=json.dumps(fin, sort_keys=True, indent=4, separators=(',', ': '))
    file1.write(dp)
file1.close()