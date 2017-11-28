#!/usr/bin/env python3
import csv
from scipy.stats.stats import pearsonr
import pdb
import sys

documents = sys.argv[4]
with open(documents) as f:
    lines = f.read().splitlines()

#with open('train_ent_spt.txt','r') as file:
#    data = file.readlines()

class_len = sys.argv[1]
classone = sys.argv[2]

#class_len =778                  # total number of docs
listclass=[]

trainfile=sys.argv[3]

with open(trainfile,'r') as file:
    data = file.readlines()

for i in range(0,int(classone)):            # No. of doc of class '0'
     listclass.append(0)

for i in range(int(classone)+1,int(class_len)+1):        # (No. of doc of class '0'+ 1) through( total number of docs+1)
     listclass.append(1)



relation = [0]*int(class_len)
for i in range(len(lines)):
        lines[i] = lines[i].split(', ')
        relid = 'R'+str(i+1)
        rel_id = ' R'+str(i+1)+'\n'
        for j in range(len(lines[i])):
             relation[int(lines[i][j])-1] = 1
        
        try:
             with open('Pearson.csv', 'a') as myfile:
                   writer = csv.writer(myfile, dialect='excel')
                   row = [relid, pearsonr(listclass, relation)[0], pearsonr(listclass, relation)[1]]    # change inv_wordlist with relation
                   
                   if pearsonr(listclass,relation)[0] >= 0.1 or pearsonr(listclass,relation)[0] <=-0.1:
                        for j in range(len(lines[i])):
                           
                            temp = data[int(lines[i][j])-1].replace("\n", "")
                            data[int(lines[i][j])-1] = temp+rel_id

                   writer.writerow(row)
        except IOError as ioe:
                         print('Error: ' + str(ioe))

with open('doc_p','w') as file:
     file.writelines(data)



                 
