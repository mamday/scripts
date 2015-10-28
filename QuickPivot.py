#! /usr/bin/env python

import numpy
import math
import sys,os

#test_list = [0,5,4,2,1,3]
file_list = open(sys.argv[1])
test_list = []
for line in file_list.readlines():
  test_list.append(int(line)) 

#test_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
global count_rec
count_rec = 0
def QSort(in_list):
  global count_rec
  if(len(in_list)>1):
    count_rec+=len(in_list)-1
    #print count_rec,in_list
    pivotl = in_list[0]
    pivotm = in_list[-1]
    pivotr = in_list[int(math.ceil((float(len(in_list))/2))-1)]
    pivot_list = sorted([pivotl,pivotm,pivotr]) 
#    pivot = pivotl
#    pivot = pivotm
    pivot = pivot_list[1] 
    p_ind = in_list.index(pivot)
    #print len(in_list),p_ind
    in_list[p_ind] = in_list[0]
    in_list[0] = pivot
    l_list = []
    r_list = []
    part_list = []
    countl = 0
    i=1
    for k in xrange(len(in_list)):
#      print countl,k
      if(k==0):
        pass
      if(in_list[k]<pivot):
        countl+=1
        cur = in_list[i]
        #print 'Bef',in_list[i],in_list[k]
        in_list[i]=in_list[k]  
        in_list[k]=cur  
        #print 'Aft',in_list[i],in_list[k]
        i+=1
    in_list[0] = in_list[i-1]
    in_list[i-1]=pivot 
    l_list = in_list[:countl]
    r_list = in_list[(countl+1):]
    l_list = QSort(l_list)
    r_list = QSort(r_list)
#    print part_list,l_list,r_list
    return l_list + [pivot] + r_list 
  else:
    return in_list

new_list = QSort(test_list)
#print count_rec,test_list,new_list
print count_rec
