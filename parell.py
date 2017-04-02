import os,string,json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords,wordnet
import multiprocessing
from multiprocessing import Process
stop =  stop= stopwords.words('english') + list(string.punctuation)
cwd=os.getcwd()
train=cwd+"/input/train/"
def info(title):
    print title
    print 'module name:', __name__
    if hasattr(os, 'getppid'):  # only available on Unix
        print 'parent process:', os.getppid()
    print 'process id:', os.getpid()

def process_folder(t):
    t=[x for x in t]
    path=t[0]
    subfolder=t[1]
    dic={}
#    info('Processing folder '+subfolder)
    filenames=path+subfolder+'/'
    for i in os.listdir(filenames):
        with open(filenames+i+'.txt','r') as file1:
            doc=file1.read()
        file1.close() 
        doc=" ".join([k for k in doc.split() if k.isalnum() or k==" " or k=="\n"])
        doc=" ".join([word.lower() for word in ndoc.split() if wordnet.synsets(word) and word not in stop ])
        dic[str(i)]=doc
    with open(os.getcwd()+r'/input/jsons/'+subfolder+r'.json','w') as file1:
        dic=json.dumps(dic, sort_keys=True, indent=4, separators=(',', ': '))
    file1.write(dic)
    file1.close()

if __name__ == '__main__':
    categories=os.listdir(train)
    pool = multiprocessing.Pool(2)
    tasks=[]
    for i in categories:
        d=[]
        d.append(train)
        d.append(i)
        d=tuple(d)
        tasks.append(d)
    results = pool.map_async(process_folder, tasks)
    pool.close()
    pool.join()
    print results