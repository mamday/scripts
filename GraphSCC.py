#! /usr/bin/env python

import numpy
import sys,os
import math
import copy
from copy import deepcopy
import collections
from collections import deque
file_name = sys.argv[1]
global graph_nodes
global graphrev_nodes
#Make obnoxiously large dictionaries to avoid having to search through keys
graph_nodes = {key: deque() for key in [str(i) for i in xrange(0,1000000)]} 
graphrev_nodes = {key: deque() for key in [str(i) for i in xrange(0,1000000)]}
 
#Comment
for line in open(file_name).readlines():
  in_list = line.split(' ')
  sec_list = line.split(' ')
  in_list = in_list[:2]
  sec_list = sec_list[:2]

  num_list = in_list+[0]+[False]
  graph_nodes[num_list[0]].append(num_list)

  sec_list.reverse()
  num_list1 = sec_list+[0]+[False]
  graphrev_nodes[num_list1[0]].append(num_list1)

print 'Loaded'
#print graphrev_nodes,graph_nodes
global sccs,all_leader,leader,count
all_leader = deque() 
#sccs = {key: [] for key in xrange(1+max([max(graph_nodes.keys()),max(graphrev_nodes.keys())]))}
sccs = {key: deque() for key in [str(i) for i in xrange(0,1000000)]} 
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
    cur_heads = deque() 
    e_bool = True
    #if(len(nodes)<1):
    #  return 0 
    #print 'Begin Awesome'
    cur_node = nodes[-1][0]
    while(e_bool):
      #print cur_node,len(g_nodes[cur_node]),e_bool
      #print 'Beg',e_bool,cur_node,cur_heads,all_leader
      if(len(g_nodes[cur_node])>leader[cur_node]):
        #print 'Explore Lead'
        exp_node = g_nodes[cur_node][leader[cur_node]]
        #print 'Explore',exp_node
        leader[cur_node]+=1
        if(exp_node[3]==False):
          #print 'Explore False'
          exp_node[3]=True
          if(leader[cur_node]==1):
            cur_heads.append(cur_node)
          if(len(g_nodes[exp_node[1]])>0):
            cur_node = exp_node[1]
          else:
            #print 'Explore Edge'
            if(not(lead>-1)):
              leader[exp_node[1]]+=1
              h_node = deque()
              h_node.append(exp_node[1])
              h_node.append(-1)
              h_node.append(0)
              h_node.append(True)
              g_nodes[exp_node[1]].append(h_node)
              all_leader.append(exp_node[1])
            cur_node = cur_heads[-1]
        else:
          #print 'Explore True',cur_node,cur_heads
          if(cur_node!=nodes[-1][0]):
            if(len(g_nodes[cur_heads[-1]])==leader[cur_heads[-1]]):
              if(len(cur_heads)>1):
                if(not(lead>-1)):
                  all_leader.append(cur_heads[-1])
                else:
                  cur_node = cur_heads[-1]
              else:
                if(not(lead>-1)):
                  all_leader.append(cur_heads[-1])
                else:
                  sccs[lead].append(cur_heads[-1])
                  #print 'SCC',lead,sccs[lead]
                e_bool = False
            else:
              cur_node = cur_heads[-1]
          else:
            e_bool = False
      else:
        #print 'Explore Full'
        if(len(cur_heads)>1):
          #next_node = g_nodes[cur_node][leader[cur_node]-1][1]
          #if(not(leader[next_node]<len(g_nodes[next_node]))):
          if(len(g_nodes[cur_heads[-1]])==leader[cur_heads[-1]]):
            if(not(lead>-1)):
              all_leader.append(cur_heads[-1])
            else:
              sccs[lead].append(cur_heads[-1])
              #print 'SCC',lead,sccs[lead]
            cur_heads.pop()
            cur_node = cur_heads[-1]
          else:
            cur_node = cur_heads[-1]
        else:
          if(len(g_nodes[cur_heads[0]])==leader[cur_heads[0]]):
            #print 'Explore Full Stop'
            if(not(lead>-1)):
              all_leader.append(cur_heads[0])
            else:
              sccs[lead].append(cur_heads[0])
              #print 'SCC',lead,sccs[lead]
            e_bool = False
          else:
            cur_node = cur_heads[0]
      #print e_bool,cur_node,cur_heads,all_leader

def FindLeaders(g_nodes):
  global all_leader,leader,count
  leader = {key: 0 for key in g_nodes.keys()} 
  count=0
  count2=0
  for ind,nodes in g_nodes.iteritems():
    count+=1
    if(len(nodes)==0 or not(False in [i[3] for i in nodes])):
#    if(len(nodes)==0 or (nodes[0][1]==-1) or (leader[ind]==len(nodes))):
      continue
#    if(len(nodes)==1 and len(g_nodes[nodes[0][1]])==0):
#      h_node = deque()
#      h_node.append(nodes[0][1])
#      h_node.append(-1)
#      h_node.append(0)
#      h_node.append(True)
#      g_nodes[nodes[0][1]].append(h_node)
#      all_leader.append(nodes[0][1])
#      continue
    count2+=1
    #print count,count2
    lead = -1 
    #leader = {key: 0 for key in g_nodes.keys()} 
    ExpNode(nodes,g_nodes,lead)
  
FindLeaders(graphrev_nodes)

print 'Found Leaders'

def FindSCC(g_nodes):
  global leader,count,all_leader
  all_leader.reverse()
  leader = {key: 0 for key in g_nodes.keys()} 
  for head in all_leader:
    #print head
    lead=head
    #leader = {key: 0 for key in g_nodes.keys()}
    if(not(False in [i[3] for i in g_nodes[head]])):
      if(not(len(g_nodes[head])>0)):
        sccs[head].append(head)
      continue
    ExpNode(g_nodes[head],g_nodes,lead)

FindSCC(graph_nodes)

#print graphrev_nodes,graph_nodes


print 'SCCs:'
for ind,scc in sccs.iteritems():
  if(len(scc)>0):
    print ind,scc,len(scc)

