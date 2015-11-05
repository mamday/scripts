#! /usr/bin/env python

import numpy
import sys,os
import math
import copy
from copy import deepcopy
file_name = sys.argv[1]
global graph_nodes
global graphrev_nodes
graph_nodes = {} 
graphrev_nodes = {} 
for line in open(file_name).readlines():
  in_list = line.split(' ')
  if(not(int(in_list[0]) in graph_nodes.keys())):
    graph_nodes[int(in_list[0])] = []
  if(not(int(in_list[1]) in graphrev_nodes.keys())):
    graphrev_nodes[int(in_list[1])] = []

  num_list = [int(i) for i in in_list if(i!=False and not(i.isspace()))]
  graph_nodes[int(in_list[0])].append(deepcopy(num_list))
  graph_nodes[int(in_list[0])][-1].append(0)
  graph_nodes[int(in_list[0])][-1].append(False)

  num_list.reverse()
  graphrev_nodes[int(in_list[1])].append(deepcopy(num_list))
  graphrev_nodes[int(in_list[1])][-1].append(0)
  graphrev_nodes[int(in_list[1])][-1].append(False)

print graphrev_nodes,graph_nodes
global all_leader,leader,count
all_leader = []

def ExpNode(nodes,g_nodes):
  global count,all_leader,leader
  for node in nodes:
    #print 'Bef',leader,count,node
    if(node[3]==False):
      node[3]=True
      #print node[0],node[1]
      if(False in [i[3] for i in g_nodes[node[1]]]):
        ExpNode(g_nodes[node[1]],g_nodes)
    else:
      continue
    leader[node[0]]+=1
    if(leader[node[0]]>=len(g_nodes[node[0]])): 
      count+=1
      node[2]=count
      all_leader.append(node[0])
      #print 'Aft',count,node    

def FindLeaders(g_nodes):
  global leader,count,all_leader
  graph_list = []
  count = 0
  leader = {key: 0 for key in g_nodes.keys()} 
  for ind,nodes in g_nodes.iteritems():
    print ind,nodes
    print ind,nodes
    #if(len(all_leader)<1 and ind!=8):
    #  continue
    ExpNode(nodes,g_nodes)
  return all_leader
leaders = FindLeaders(graphrev_nodes)
print graphrev_nodes,graph_nodes
