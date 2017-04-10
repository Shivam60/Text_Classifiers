import os
path=r'/home/shivam/Programing/Current_Projects/Document_Classification_dataset/Data_Set/379/train/'
folders=os.listdir(path)
a=0
for i in folders:
    for j in os.listdir(path+r'/'+i):
        os.rename(path+r'/'+i+r'/'+j,path+r'/'+i+r'/'+j+'.txt')
print a
