import os,string,json,time,multiprocessing,enchant,sys
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from multiprocessing import Pool
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool 
words=enchant.Dict("en_US")
stop = stopwords.words('english') + list(string.punctuation)
def vocap_category(arg):
    files=[]
    global bag
    path=arg[0]
    threads=int(arg[1])
    folder_name=path.split('/')
    folder_name=folder_name[len(folder_name)-2]
    try: 
        with open(os.getcwd()+r'/input/jsons/train-multi.json','r') as file1:
            bag=file1.read()
            bag=json.loads(bag)
            file1.close()
    except IOError as e:
        print e
    try: 
        with open(os.getcwd()+r'/input/jsons/'+str(folder_name)+r'.json','r') as file1:
            dp=file1.read()
            dp=json.loads(dp)
            file1.close()
    except e as err:
        print e

    itter=[]
    for i in dp:
        for j in dp[i]:
            itter.append([str(i),str(j)])
    pool = ThreadPool(threads) 
    results = pool.map(vocap_subfile,itter)
    a=set()
    for i in results:
        a=a.union(i)
    return a
def vocap_subfile(arg):
    category_name=arg[0]
    file_name=arg[1]
    a=bag[category_name][file_name].split() 
    return set(a)
def process_folder(arg):
    files=[]
    path=arg[0]
    threads=int(arg[1])
    folder_name=path.split('/')
    folder_name=folder_name[len(folder_name)-2]
    d={}
    print "Enter ",folder_name
    for i in os.listdir(path):
        files.append(path+i)
    pool = ThreadPool(threads) 
    results = pool.map(process_file,files)
    a={}
    for i in results:
        a.update(i)
    d[folder_name]=a

   # print folder_name,len(d[folder_name]),"files Indexed"
    with open(os.getcwd()+r'/input/jsons/'+str(folder_name)+r'.json','w') as file1:
        dp=json.dumps(d, sort_keys=True, indent=4, separators=(',', ': '))
        file1.write(dp)
        file1.close()
    return 1
def process_file(filename):
    d={}
    file_name=filename.split('/')
    file_name=file_name[len(file_name)-1]
    print "Enter ",file_name
    try:
        with open(filename,'r') as file1:
            doc=file1.read()
    except IOError as err:
        print err
    finally:
        file1.close()
    doc=" ".join([k for k in doc.split() if k.isalnum() or k==" " or k=="\n"])
    doc=" ".join([word for word in doc.split() if word not in stop and words.check(word)])
    doc=" ".join([k.lower() for k in doc.split()])
    d[file_name]=doc
    print "Exit ",file_name
    return d
def join_JSON():
    bag={}
    json_files = [pos_json for pos_json in os.listdir(os.getcwd()+r'/input/jsons') if pos_json.endswith('.json')]
    for i in json_files:
        with open(os.getcwd()+r'/input/jsons/'+str(i),'r') as file1:
            dp=file1.read()
            dp2=json.loads(dp)
            a=0
            #print 1
            for j in dp2:
                #print j
                bag[str(i)]=dp2[j]
            file1.close()
    with open(os.getcwd()+r'/input/jsons/train-multi.json','w') as file1:
        bag=json.dumps(bag, sort_keys=True, indent=4, separators=(',', ': '))
        file1.write(bag)

if __name__ == '__main__':
    start=time.time()
    #processes_limit=int(sys.argv[1])
    #threads=int(sys.argv[2])
    processes_limit=3
    threads=30
    print "Program started at: ",start
    print "Number of Processors used: ", processes_limit
    print "Number of Threads used: ", threads
    cwd=os.getcwd()
    train=cwd+r"/input/train/"
    categories=os.listdir(train)
    itter=[]
    for i in range(0,len(categories)):
        itter.append([train+categories[i]+r'/',threads])
    p = Pool(processes=processes_limit)
    results=p.map(process_folder, itter)
    #code to combine all jsons
    join_JSON()
    #code to make vocabulary
    #p = Pool(processes=processes_limit)
    #results=p.map(vocap_category, itter)
    ans=set()
    end=time.time()
    print "Program ended at: ",end
    print "Total Time to process: ",end-start
    sys.exit(end-start)
