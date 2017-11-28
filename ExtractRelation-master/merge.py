#!/usr/bin/env python3

import pdb
import csv
import sys

tlist=[]
trainlist = []
#Contains Relations from Test documents. [NE1] [NE2]

inputfile = sys.argv[1]
with open(inputfile) as csvfile:
     spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
     for row in spamreader:
         tlist.append(row)


prev1 = tlist[0][0]
prev2 = tlist[0][1]
dellist = []
flag = 0
       
for i in range(1,len(tlist)):
       if tlist[i][0] == prev1  and tlist[i][1] == prev2:        #temp2[temp1.index(testlist[i][0])]:
              tlist[i][2]=tlist[i][2]+tlist[i-1][2]
              dellist.append(i-1)   
       prev1 = tlist[i][0]
       prev2 = tlist[i][1]
       
         


for n in range(len(dellist)-1, -1,-1):
      tlist.pop(dellist[n])

for item in tlist:
     try:
        with open('Relmerged.csv', 'a') as myfile:
            writer = csv.writer(myfile, delimiter = '\t')
            writer.writerow([item[0]]+[item[1]]+[item[2]]+[item[3]])

     except IOError as ioe:
         print('Error: ' + str(ioe))  
           
