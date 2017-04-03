import os,string,json,time,multiprocessing,enchant,threading
from threading import Thread
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from multiprocessing import Process
bag={}

words=enchant.Dict("en_US")
stop = stopwords.words('english') + list(string.punctuation)
cwd=os.getcwd()
train=cwd+r"/input/train/"
def process_file(t):
    dic={}
    t=[x for x in t]
    subfile=t[0]
    subfolder=t[1]
    path=t[2]
    try:
        with open(path+subfile,'r') as file1:
            doc=file1.read()
    except IOError as err:
        print "{0}".format(err)
    finally:
        file1.close()
    doc=" ".join([k for k in doc.split() if k.isalnum() or k==" " or k=="\n"])
    doc=" ".join([word.lower() for word in doc.split() if word not in stop and words.check(word) ])
    bag[str(subfile)]=doc
    print doc

def process_folder(t):

    t=[x for x in t]
    path=t[0]
    subfolder=t[1]
    filenames=path+subfolder+r'/'
    fl=[]
    for i in os.listdir(filenames):
        d=[]
        d.append(i)
        d.append(subfolder)
        d.append(filenames)
        d=tuple(d)
        fl.append(d)   
    lis=[]
    for i in fl:
        th = Thread(target=process_file, args=(i,))
        th.start()
        lis.append(th)
    for i in lis:
        i.join()
    print bag
    sys.stdout.flush()
    try:
        with open(os.getcwd()+r'/input/jsons/train-multi-prallel.json','w') as file1:
            bag=json.dumps(bag, sort_keys=True, indent=4, separators=(',', ': '))
            file1.write(bag)
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
        bag[i]={}
    results = pool.map_async(process_folder, tasks)
    pool.close()
    pool.join()
    end=time.time()

    print "Program ended at: ",end
    print "Total Time to process: ",end-start
