import multiprocessing,os
from multiprocessing import Process
cwd=os.getcwd()
train=cwd+r"/input/train/"
def process_folder(t):
    t=[x for x in t]
    path=t[0]
    subfolder=t[1]
    dic={}
    filenames=path+subfolder+r'/'
    for i in os.listdir(filenames):
        try:
            with open(filenames+str(i),'r') as file1:
                doc=file1.read()
        except IOError as err: 
            print "{0}".format(err)
        finally:
            file1.close() 
        print doc
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