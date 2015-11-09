#! /usr/bin/env python

import numpy
import sys,os
import math
import copy
from copy import deepcopy
file_name = sys.argv[1]
global graph_nodes
global graphrev_nodes
graph_nodes = {key: [] for key in xrange(0,1000000)} 
graphrev_nodes = {key: [] for key in xrange(0,1000000)}
 
for line in open(file_name).readlines():
  in_list = line.split(' ')
  in_list = in_list[:2]
#  try:
#    for i in in_list:
#      if(i!='\n'):
#        int(i)
#  except:
#    print 'Failed',in_list,line
  num_list = [int(i) for i in in_list if(i!=False and (i.isdigit() or not(i.isspace())))]
  graph_nodes[int(in_list[0])].append(deepcopy(num_list))
  graph_nodes[int(in_list[0])][-1].append(0)
  graph_nodes[int(in_list[0])][-1].append(False)

  num_list.reverse()
  graphrev_nodes[int(in_list[1])].append(deepcopy(num_list))
  graphrev_nodes[int(in_list[1])][-1].append(0)
  graphrev_nodes[int(in_list[1])][-1].append(False)

print 'Loaded'
#print graphrev_nodes,graph_nodes
global sccs,all_leader,leader,count
all_leader = []
sccs = {key: [] for key in xrange(1+max([max(graph_nodes.keys()),max(graphrev_nodes.keys())]))}
#Today I learned that recursion is not always a good idea
def RecExpNode(nodes,g_nodes,lead):
  global count,sccs,all_leader,leader
  for node in nodes:
    #print 'Bef',leader,count,node
    if(node[3]==False):
      node[3]=True
      if(len(g_nodes[node[1]])>0):
        #print g_nodes[node[1]] 
        if(False in [i[3] for i in g_nodes[node[1]]]):
          RecExpNode(g_nodes[node[1]],g_nodes,lead)
      else:
        #print node[0],node[1]
        if(not(lead>-1)):
          count+=1
          all_leader.append(node[1])
    else:
      continue
    leader[node[0]]+=1
    if(leader[node[0]]>=len(g_nodes[node[0]])): 
      count+=1
      node[2]=count
      if(not(lead>-1)):
        all_leader.append(node[0])
      else:
        sccs[lead].append(node[0])
      #print 'Aft',sccs,count,node    

def ExpNode(nodes,g_nodes,lead):
    global count,sccs,all_leader,leader
    in_heads = [i[0] for i in nodes]
    in_tails = []
    cur_heads = [] 
    e_bool = True
    cur_node = in_heads[0]
    while(e_bool):
      exp_node = g_nodes[cur_node][leader[cur_node]]
      leader[cur_node]+=1
      #TODO exp_node here can be multiple edges also
      if(exp_node[3]==False):
        exp_node[3]==True
        count+=1
        cur_heads.append(cur_node)
        if(len(g_nodes[exp_node[1]])>0):
          cur_node = exp_node[1]
        else:
          for i in xrange(len(cur_heads)):
         #TODO won't work right now because g_nodes[i] might be multiple edges
            if(g_nodes[i][2]>count):
              g_nodes[i][2]=count
            count-=1
            e_bool = False
      else:
        for i in xrange(len(cur_heads)):
          #TODO won't work right now because g_nodes[i] might be multiple edges
          if(g_nodes[i][2]>count):
            g_nodes[i][2]=count
          count-=1
          e_bool = False

def FindLeaders(g_nodes):
  global leader,count
  count = 0
  leader = {key: 0 for key in g_nodes.keys()} 
  lead = -1 
  for ind,nodes in g_nodes.iteritems():
    ExpNode(nodes,g_nodes,lead)
  
FindLeaders(graphrev_nodes)
print 'Found Leaders'

#def FindSCC(g_nodes):
#  global leader,count,all_leader
#  count = 0
#  leader = {key: 0 for key in g_nodes.keys()}
#  all_leader.reverse()
#  for head in all_leader:
#    lead=head
#    if(not(len(g_nodes[head])>0)):
#      sccs[head].append(head)
#    else:
#      ExpNode(g_nodes[head],g_nodes,lead)

FindSCC(graph_nodes)
#print graphrev_nodes,graph_nodes

#print 'SCCs:'
#for ind,scc in sccs.iteritems():
#  if(len(scc)>0):
#    print ind,scc,len(scc)
