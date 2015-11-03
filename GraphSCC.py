#! /usr/bin/env python

import numpy
import sys,os
import math
import copy
from copy import deepcopy
file_name = sys.argv[1]
global graph_nodes
graph_nodes = {} 
for line in open(file_name).readlines():
  in_list = line.split(' ')
  if(not(int(in_list[0]) in graph_nodes.keys())):
    graph_nodes[int(in_list[0])] = []
  graph_nodes[int(in_list[0])].append([int(i) for i in in_list if(i!=False and not(i.isspace()))])
  graph_nodes[int(in_list[0])][-1].append(0)
  graph_nodes[int(in_list[0])][-1].append(False)

#print len(graph_nodes),graph_nodes
global all_leader,leader,count
all_leader = []
def ExpNode(nodes):
  global count,leader,graph_nodes
  for node in nodes:
    #print 'Bef',leader,count,node
    if(node[3]==False):
      node[3]=True
      #print node[0],node[1]
      if(False in [i[3] for i in graph_nodes[node[1]]]):
        ExpNode(graph_nodes[node[1]])
    else:
      continue
    leader[node[0]]+=1
    if(leader[node[0]]>=len(graph_nodes[node[0]])): 
      count+=1
      node[2]=count
      #print 'Aft',count,node    

def FindSCC(graph_nodes):
  global leader,count,all_leader
  max_list = []
  graph_list = []
  for ind,nodes in graph_nodes.iteritems():
    leader = {key: 0 for key in graph_nodes.keys()} 
    count = 0
    if(not(ind in all_leader)):
#    print 'FindSCC',nodes
      #if(ind!=7 and ind!=1):
      #  continue
      all_leader.append(ind)
      ExpNode(nodes)
      new_nodes = deepcopy(graph_nodes)
      graph_list.append(new_nodes)
      print 'SCC',ind,all_leader
      max_val = 0
      for ind1,nodes1 in graph_nodes.iteritems():
        for node1 in nodes1:
          node1[3]=False
          if(node1[2]>max_val):
            max_val = node1[2]
          node1[2]=0
      max_list.append(max_val)
  print max_list,max(max_list),graph_list[max_list.index(max(max_list))] 
FindSCC(graph_nodes)
