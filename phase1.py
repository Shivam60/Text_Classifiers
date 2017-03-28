import os,string,json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords,wordnet

stop =  stop= stopwords.words('english') + list(string.punctuation)
cwd=os.getcwd()
tests=cwd+"/input/test/"
categories=os.listdir(tests)
bag={}
for i in categories:
    col={}
    filenames=tests+i+"/"
    for j in os.listdir(filenames):
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
        col[j]=tmp1
    bag[i]=col
with open(os.getcwd()+r'/input/jsons/'+r'test.json','w') as file1:
    dp=json.dumps(bag, sort_keys=True, indent=4, separators=(',', ': '))
    file1.write(dp)
file1.close()