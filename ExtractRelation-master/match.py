#!/usr/bin/env python3

import pdb
import csv

testlist=[]
trainlist = []
#Contains Relations from Test documents. [NE1] [NE2]
with open('testRelationpoltech200.csv') as csvfile:
     spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
     for row in spamreader:
         testlist.append(row)


# This excel contains relations extracted from the training documents.
# [Relation id]  [NE1]	[NE2]
with open('trainRelpoltech200.csv') as csvfile:
     spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
     for row in spamreader:
         trainlist.append(row)

count = 0
temp1 = [row[1] for row in trainlist]  #Stores NE1s
temp2 = [row[2] for row in trainlist]  #Stores NE2s
matched = []

for i in range(len(testlist)):

       if testlist[i][0] in temp1  and testlist[i][1] == temp2[temp1.index(testlist[i][0])]:
              count = count + 1
              
              print i 
              val=temp1.index(testlist[i][0])  
              print val
              print trainlist[val][0] 
              matched.append(trainlist[val][0])

       else:
              matched.append('')
 
file = open("Relmatched.txt", "w")
for item in matched:
  file.write("%s\n" % item)  
           
print "Relations Matched", count
