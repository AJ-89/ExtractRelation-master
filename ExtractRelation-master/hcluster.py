from numpy import * 
from PIL import Image,ImageDraw
import pdb

class cluster_node:
    def __init__(self,vec,convec =0, left=None,right=None,distance=0.0,id=None,count=1):
        self.left=left
        self.right=right
        self.vec=vec
        self.convec = convec
        self.id=id
        self.distance=distance
        self.count=count #only used for weighted average 

def L2dist(v1,v2):
    return sqrt(sum((v1-v2)**2))

def intersect(a,b):
    return list(set(a) & set(b))

def hcluster(features,conveclist,distance=L2dist):
    #cluster the rows of the "features" matrix
    distances={}
    #currentclustid=-1
    min_element = []
    
    merge_rows = []
    # clusters are initially just the individual rows
    clust=[cluster_node(array(features[i],dtype =float ),id=i,convec = conveclist[i]) for i in range(len(features))]
    while len(clust)>1:
        lowestpair=(0,1)
        maximum=-1
        #closest=distance(clust[0].vec,clust[1].vec)

        # loop through every pair looking for the smallest distance
        for i in range(1,len(clust)):
           # for j in range(i+1,i+2):
            for j in range(i):
                # distances is the cache of distance calculations
                if (clust[i].id,clust[j].id) not in distances: 
                    distances[(clust[i].id,clust[j].id)]= clust[i].vec[j]

                d=distances[(clust[i].id,clust[j].id)]

                if d > maximum and d > 0 :
                    maximum =d
                    lowestpair=(i,j)
        
        # if the matrix has no positive value set min to 0
        if maximum == -1:
            maximum = 0 
        
        if maximum <  0.25:    # Consider jaccard similarity value greater than equal to  0.25
            break 
        
        #pdb.set_trace() 
        #print intersect(clust[lowestpair[0]].vec , clust[lowestpair[1]].vec)

  
        # calculate the avg between the two rows with the minimum element
        mergevec= []
        min_element.append(round(maximum,3))
        low = lowestpair[0]
        high = lowestpair[1]
        if lowestpair[0] > lowestpair[1]:
             low = lowestpair[1]
             high = lowestpair[0]
        for k in range(len(clust[high].vec)):
             if k != low and  k != high:
                  
                  if k <= len(clust[low].vec)-1:
                      a = clust[low].vec[k] 
                  else:
                      a = clust[k].vec[low] 
                  b = clust[high].vec[k]
                  
                  mergevec.append(float(a+b)/2.0)
       
        mergevec.append(0) 
        # create the new cluster
        #currentclustid = [clust[lowestpair[0]].id,clust[lowestpair[1]].id]
        currentclustid =''.join([str(clust[lowestpair[0]].id),',',str(clust[lowestpair[1]].id)])
        newcluster = cluster_node(array(mergevec), convec =intersect(clust[lowestpair[0]].convec,clust[lowestpair[1]].convec) ,left = clust[lowestpair[0]],right = clust[lowestpair[1]], distance = maximum, id = currentclustid) 
        
        #merge_row = [clust[lowestpair[0]].id, clust[lowestpair[1]].id]
        #merge_rows.extend(merge_row)
        

        # reorganize the other clusters or rows
        for k in range(low+1, len(clust)):
            if k != high and k> high: 
               flag = 0
               int_merge = 0.0
               for m in range(len(clust[k].vec)):
                 idx = m
                
                 if m == low or m == high:
                    if flag == 1:
                       idx = m-1
       
                    int_merge += float(clust[k].vec[idx])
 
                    clust[k].vec=delete(clust[k].vec,idx)
                    flag = 1                      
               if k > high:
                  clust[k].vec=insert(clust[k].vec,high-1, round(float(int_merge)/2.0,3) )               
            elif k <high:
                for m in range(len(clust[k].vec)):
                  if m == low:
                    clust[k].vec   = delete(clust[k].vec,m)
        # cluster ids that weren't in the original set are negative
        #currentclustid-=''.join([str(i),',',str(j)])
        clust[high] = newcluster
        del clust[low]
        #clust.append(newcluster)
         
        merge_row = newcluster.convec
        merge_rows.append(merge_row)

        #print merge_row 
        #for p in range(len(clust)):
        #    print  clust[p].id
        #    print  clust[p].vec

        #print ('\n\n')
    #print min_element
    return merge_rows 

