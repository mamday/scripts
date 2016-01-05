#! /usr/bin/env python

import numpy
import math
import sys,os
import copy
from copy import deepcopy
file_name = sys.argv[1]
n_dict = {}
for line in open(file_name).readlines():
  l_split = line.split(' ')
  if((str(l_split[0]) in n_dict) and n_dict[str(l_split[0])]!=None):
    n_dict[str(l_split[0])]+=[[str(l_split[2]),int(l_split[4])]]
    if((str(l_split[2]) in n_dict)):
      n_dict[str(l_split[2])]+=[[str(l_split[0]),int(l_split[4])]]
    else:
      n_dict[str(l_split[2])]=[[str(l_split[0]),int(l_split[4])]]
  else:
    n_dict[str(l_split[0])] = [[str(l_split[2]),int(l_split[4])]]
    if((str(l_split[2]) in n_dict)):
      n_dict[str(l_split[2])]+=[[str(l_split[0]),int(l_split[4])]]
    else:
      n_dict[str(l_split[2])]=[[str(l_split[0]),int(l_split[4])]]

for key,lis in n_dict.iteritems():
  if(n_dict[key]!=None):
    n_dict[key]+=[numpy.inf,0]
  else:
    n_dict[key]=[numpy.inf,0]
#print 'All',n_dict

#Simple debugger
#for s in xrange(len(n_dict)):
#  if(len(n_dict[s+1])>2):
#    print min([i[1] for i in n_dict[s+1][:-2]])
#  print n_dict[s+1]
def NodeDists(start,n_dict):
  count=0
  n_dict1 = deepcopy(n_dict)
  #Set initial node distance to zero
  n_dict1[start][-2]=0
  #Iterate through nodes to find distances
  h_list = [[start,0]] + n_dict1[start][:-2]
  n_dict1[start]=n_dict1[start][-2:]
  c_dist = n_dict1[start][-2] 
  d_node = start 
  #print 'The list',h_list
#  while(len(h_list)>0):
  while(count<15):
    count+=1
  #Update the distance for all the edges
    for edge in h_list: 
      if(n_dict1[edge[0]][-2]>(edge[1])):
        n_dict1[edge[0]][-2]=edge[1]
        n_dict1[edge[0]][-1]=d_node
      #print 'Nodes',edge[0],n_dict1[edge[0]]
    d_list = [i[1] for i in h_list]
    #print 'Bef',d_list
  #Try to remove the current nodes from the queue
    for ind,val in enumerate(d_list):
      if(val==c_dist):
        print len(d_list),len(h_list),count,val,c_dist
        try:
          c_ind = ind
          del h_list[c_ind]      
          del d_list[c_ind]      
        except:
          print 'Weird Fail',c_ind,d_list,h_list
          break 
    print 'Aft',d_list,len(d_list)
  #Get the new distance and node
    if(len(d_list)>0):
      c_dist = min(d_list)
      #print 'Min',c_dist,count
      for ind,val in enumerate(h_list):
        if(val[1]==c_dist):
          d_node = h_list[ind][0]
          else:
            n_list.append(d_node)
          #If there are nodes that haven't been added to the queue add them
          if(len(n_dict1[d_node])>2):
            new_list = n_dict1[d_node][:-2]
            n_dict1[d_node]=n_dict1[d_node][-2:]
          for l in new_list:
            l[1]+=c_dist
          print 'New',count,ind,h_list,new_list
          h_list+=new_list
  print 'End',sum([lis[0] for key,lis in n_dict1.iteritems() if lis[0]<numpy.inf]),{key: lis[0] for key,lis in n_dict1.iteritems() if lis[0]<numpy.inf}
  return sum([lis[0] for key,lis in n_dict1.iteritems() if lis[0]<numpy.inf])

dists = []
for key,lis in n_dict.iteritems():
  d_val = NodeDists(key,n_dict)
  dists.append(d_val)
print dists,min(dists)
