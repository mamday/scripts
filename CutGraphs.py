#! /usr/bin/env python

import sys,os
import numpy
import math
from numpy import random
import copy
from copy import deepcopy
file_name = sys.argv[1]
in_graph = {}
for line in open(file_name).readlines():
  in_arr=line.split('	')
#  in_arr=line.split(' ')
  num_arr = [int(i) for i in in_arr if(not(i.isspace()))]
  in_graph[num_arr[0]]=num_arr[1:]
print in_graph
#test_graph = {1:[2,3,4,7],
#2:[1,3,4],
#3:[1,2,4],
#4:[1,2,3,5],
#5:[4,6,7,8],
#6:[5,7,8],
#7:[1,5,6,8],
#8:[5,6,7]}

#print numpy.random.choice(test_graph.keys()),test_graph.keys(),test_graph[1],test_graph[2]
def GCut(test_graph):
  while(len(test_graph)>2):
    d_num = numpy.random.choice(test_graph.keys())
    l_num = numpy.random.choice(test_graph[d_num])
    #print 'Bef',test_graph,d_num,l_num
    while l_num in test_graph[d_num]:
      test_graph[d_num].remove(l_num)
    while d_num in test_graph[l_num]:
      test_graph[l_num].remove(d_num)
    test_graph[d_num].extend(test_graph[l_num])
    test_graph.pop(l_num,None)
    for i,j in test_graph.iteritems():
      if i==d_num:
        pass
      if l_num in j:
#       if d_num in j:
#         j.remove(d_num)
         while(l_num in j):
           j[j.index(l_num)]=d_num
  #print 'Aft',d_num,l_num,len(test_graph),test_graph
min_val = 9999 
for i in xrange(1000):
  test_graph = deepcopy(in_graph)
  GCut(test_graph)
  for i,j in test_graph.iteritems():
    if(len(j)<min_val):
      min_val=len(j) 
print min_val 
