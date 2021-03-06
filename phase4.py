import os,string,json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords,wordnet

stop =  stop= stopwords.words('english') + list(string.punctuation)
cwd=os.getcwd()
test=cwd+"/input/test/"
categories=os.listdir(test)
bag={}
cnt=0
for i in categories:
    col={}
    filenames=test+i+"/"
    for j in os.listdir(filenames):
        print i, "Processing File: ",j,". Number of Files Processed: ",cnt
        tmp1=[]
        with open(filenames+j,'r') as file1:
            doc=file1.read()
            ndoc="" 
            for k in doc:
                if k.isalnum() or k==" " or k=="\n":
                    ndoc+=k
            doc=""
            for word in ndoc.split():
                if wordnet.synsets(word) and word not in stop:
                    doc+=word.lower()+" "
            tmp1.append(doc)
        file1.close()
        col[str(i)+"_"+str(j)]=tmp1
        cnt+=1
    bag[i]=col
#    print bag
with open(os.getcwd()+r'/input/jsons/'+r'test.json','w') as file1:
    dp=json.dumps(bag, sort_keys=True, indent=4, separators=(',', ': '))
    file1.write(dp)
file1.close()