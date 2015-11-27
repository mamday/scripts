# /usr/bin/env python

import numpy
import sys,os
import math

fname = sys.argv[1]
cur_med = -1
med_list = []
all_list = []
for line in open(fname).readlines():
#  if(len(all_list)>10):
#    break
  lheap = -1 
  hheap = numpy.inf 
  lcount = 0
  hcount = 0
  cur_line = int(line)
  all_list.append(cur_line)
  if(cur_med==-1): 
    cur_med = cur_line
  else:
    for num in all_list:
      if(num==cur_med):
        continue
      if(num<cur_med):
        lcount+=1
        if(num>lheap):
          lheap=num 
      else:
        hcount+=1
        if(num<hheap):
          hheap=num 
    if(hcount>lcount):
      lheap=cur_med
      lcount+=1
    else:
      hheap=cur_med
      hcount+=1
    if(hcount>lcount):
      cur_med=hheap
    else:
      cur_med=lheap
  med_list.append(cur_med)

print 'Sum',sum(med_list),sum(med_list)%10000
