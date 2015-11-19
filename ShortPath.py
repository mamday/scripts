#! /usr/bin/env python

import numpy
import math
import sys,os

file_name = sys.argv[1]
n_dict = {key: None for key in xrange(1000)}
for line in open(file_name).readlines():
  l_split = line.split('	')
  n_dict[int(l_split[0])] = [[int(k) for k in i.split(',')] for i in l_split if ',' in i]+[numpy.inf]+[0]

for key,lis in n_dict.iteritems():
  if(not(lis)):
    n_dict[key]=[numpy.inf,0]

#Set initial node distance to zero
n_dict[1][-2]=0

#Simple debugger
#for s in xrange(len(n_dict)):
#  if(len(n_dict[s+1])>2):
#    print min([i[1] for i in n_dict[s+1][:-2]])
#  print n_dict[s+1]

#Iterate through nodes to find distances
h_list = [[1,0]] + n_dict[1][:-2]
n_dict[1]=n_dict[1][-2:]
c_dist = n_dict[1][-2] 
d_node = 1
print h_list
while(len(h_list)>0):
#Update the distance for all the edges
  for edge in h_list: 
    if(n_dict[edge[0]][-2]>(edge[1])):
      n_dict[edge[0]][-2]=edge[1]
      n_dict[edge[0]][-1]=d_node
  d_list = [i[1] for i in h_list]
  #print 'Bef',h_list,d_list
#Try to remove the current node from the queue
  try:
    c_ind = d_list.index(c_dist)
    del h_list[c_ind]      
    del d_list[c_ind]      
  except:
    print 'Weird Fail',c_ind,d_list,h_list
    break 
  #print 'Aft',h_list,d_list,n_dict
#Get the new distance and node
  if(len(d_list)>0):
    c_dist = min(d_list)
    d_node = h_list[d_list.index(c_dist)][0]
#If there are nodes that haven't been added to the queue add them
  if(len(n_dict[d_node])>2):
    new_list = n_dict[d_node][:-2]
    n_dict[d_node]=n_dict[d_node][-2:]
    for l in new_list:
      l[1]+=c_dist
    h_list+=new_list

print {key: lis[0] for key,lis in n_dict.iteritems() if lis[0]<numpy.inf}
