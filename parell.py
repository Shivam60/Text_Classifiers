import os,string,json,time
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords,wordnet
import multiprocessing
from multiprocessing import Process
bag={}
stop =  stop= stopwords.words('english') + list(string.punctuation)
cwd=os.getcwd()
train=cwd+r"/input/train/"
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
    #info('Processing folder '+subfolder)
    filenames=path+subfolder+r'/'
    for i in os.listdir(filenames):
        try:
            with open(filenames+i,'r') as file1:
                doc=file1.read()
        except IOError as err: 
            print "{0}".format(err)
        finally:
            file1.close()
        doc=" ".join([k for k in doc.split() if k.isalnum() or k==" " or k=="\n"])
        doc=" ".join([word.lower() for word in doc.split() if wordnet.synsets(word) and word not in stop ])
        dic[str(i)]=doc
    try:
        with open(os.getcwd()+r'/input/jsons/'+subfolder+r'.json','w') as file1:
            dic=json.dumps(dic, sort_keys=True, indent=4, separators=(',', ': '))
            file1.write(dic)
    except IOError as err: 
        print "{0}".format(err)
    finally:
        file1.close()

if __name__ == '__main__':
    start=time.time()
    print "Program started at: ",start
    categories=os.listdir(train)
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
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
    files=os.listdir(os.getcwd()+r'/input/jsons/',)
    for i in files:
        try:
            with open(os.getcwd()+r'/input/jsons/'+i,'r') as file1:
                dp=file1.read()
        except IOError as err: 
            print "{0}".format(err)
        except:
            print 1
        finally:
            file1.close()
        b=json.loads(dp)
        bag[i]=b
    try:
        with open(os.getcwd()+r'/input/jsons/train-parallel.json','w') as file1:
            dic=json.dumps(bag, sort_keys=True, indent=4, separators=(',', ': '))
            file1.write(dic)
    except IOError as err: 
        print "{0}".format(err)
    finally:
        file1.close()
    end=time.time()
    print "Program ended at: ",end
    print "Total Time to process: ",end-start