#! /usr/bin/env python

import numpy
import sys,os

f_name = sys.argv[1]

inf_file = open(f_name)
num_list = []
for line in inf_file.readlines():
  num_list.append(int(line))

#test_list = [0,3,4,2,1,5]
#test_list = [5,4,3,2,1,0]

global counter
counter = 0 
def MSort(in_list):
  global counter 
  if(len(in_list)>1):
    l_list = in_list[:(len(in_list)/2)]
    r_list = in_list[(len(in_list)/2):]
    l_list = MSort(l_list)
    r_list = MSort(r_list)
    o_list = []
    i=0
    j=0
    for k in xrange(len(in_list)):
      #print 'Beg',k,o_list,l_list,r_list,in_list
      if(i==len(l_list)):
        while(j<len(r_list)):
          o_list.append(r_list[j])
          j+=1
          #print 'LEnd',o_list
        continue
      if(j==(len(r_list))):
        #counter+=((j-i)-1)*j
        #print counter
        while(i<len(l_list)):
          o_list.append(l_list[i])
          i+=1
          #print 'REnd',o_list
        continue 
      if (l_list[i] < r_list[j]):
        o_list.append(l_list[i])
        i+=1
        #print 'Left',o_list
        continue 
      if (l_list[i] > r_list[j]):
        o_list.append(r_list[j])
        j+=1
        counter+=(len(l_list)-i)
        #print 'In count'
        #print counter
        #print 'Right',o_list
        continue 
    return o_list
  else:
    return in_list 
myf_list = MSort(num_list)

print 'After',myf_list
print 'After',len(myf_list),counter
