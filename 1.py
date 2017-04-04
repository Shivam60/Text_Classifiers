import threading,os,string,json,time,multiprocessing,enchant,Queue
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool 
words=enchant.Dict("en_US")
stop = stopwords.words('english') + list(string.punctuation)
cwd=os.getcwd()
train=cwd+r"/input/train/"
bag={}
def process_folder(path):
    d={}
    files=os.listdir(path)
    for i in range(0,len(files)):
        files[i]=train+files[i]
    try:
        swamp=ThreadPool(len(files)) 
        lotus=pool.map(process_file,files)
    except:
        print 1
    finally:
        swamp.close() 
        swamp.join()
    path_split=path.split('/')
    folder_name=path_split[len(path_split)-1]
    d[folder_name]={}    
    for i in lotus:
        a=i.keys()
        d[folder_name][a[0]]=i[a[0]]
    return d


def process_file(path):
    print path
    d={}
    try:
        with open(path,'r') as file1:
            doc=file1.read()
    except IOError as err:
        print err
    finally:
        file1.close()
    doc=" ".join([k for k in doc.split() if k.isalnum() or k==" " or k=="\n"])
    doc=" ".join([word.lower() for word in doc.split() if word not in stop and words.check(word)])
    path_split=path.split('/')
    d[path_split[len(path_split)-1]]=doc
    return d

if __name__ == '__main__':
    bag={}
    start=time.time()
    print "Program started at: ",start
    categories=os.listdir(train)
    for i in range(0,len(categories)):
        categories[i]=train+categories[i]
    pool = ThreadPool(len(categories)) 
    results = pool.map(process_folder,categories)
    pool.close() 
    pool.join()
    print results
    try:
        with open(os.getcwd()+r'/input/jsons/train-multi-prallel.json','w') as file1:
            bag=json.dumps(bag, sort_keys=True, indent=4, separators=(',', ': '))
            file1.write(bag)
    except IOError as err: 
        print "{0}".format(err)
    finally:
        file1.close()
    print "Program ended at: ",end
    print "Total Time to process: ",end-start
    
