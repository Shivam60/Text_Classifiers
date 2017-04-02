import os,string,json,time
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords,wordnet

stop =  stop= stopwords.words('english') + list(string.punctuation)
cwd=os.getcwd()
train=cwd+"/input/train/"
categories=os.listdir(train)
bag={}
cnt=0
start=time.time()
print "Program started at: ",start
for i in categories:
    col={}
    filenames=train+i+"/"
    for j in os.listdir(filenames):
       # print i, "Processing File: ",j,". Number of Files Processed: ",cnt
        tmp1=[]
        with open(filenames+j,'r') as file1:
            doc=file1.read()
            '''
            ndoc="" 
            #ndoc=" ".join([k for k in doc.split() if k.isalnum() or k==" " or k=="\n"])
            for k in doc:
                if k.isalnum() or k==" " or k=="\n":
                    ndoc+=k
            doc=""
            #" ".join([word.lower() for word in ndoc.split() if wordnet.synsets(word) and word not in stop ])
            for word in ndoc.split():
                if wordnet.synsets(word) and word not in stop:
                    doc+=word.lower()+" "
            '''
            doc=" ".join([k for k in doc.split() if k.isalnum() or k==" " or k=="\n"])
            doc=" ".join([word.lower() for word in doc.split() if wordnet.synsets(word) and word not in stop ])                    
            tmp1.append(doc)
        file1.close()
        col[str(i)+"_"+str(j)]=tmp1
        cnt+=1
    bag[i]=col
#    print bag
with open(os.getcwd()+r'/input/jsons/'+r'train-series.json','w') as file1:
    dp=json.dumps(bag, sort_keys=True, indent=4, separators=(',', ': '))
    file1.write(dp)
file1.close()
end=time.time()
print "Program ended at: ",end
print "Total Time to process: ",end-start