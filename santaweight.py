import sys,os
import math,numpy

in_file = sys.argv[1]
w_list = []

for line in open(in_file).readlines():
  w_list.append(int(line.strip()))

g_weight = sum(w_list)/3

comb_list = []
#Find all combinations that add up to 1/3 of the total weight
for i1,w in enumerate(w_list):
  cur_combs = []
  for i2,ow in enumerate(w_list):
    if(i2!=i1):
      new_combs = []
#Add combinations to current sum(w_list)/3 sets
      for com in cur_combs:
        if((sum(com)+ow)<=g_weight):
          new_combs.append(com+[ow]) 
      cur_combs=cur_combs+new_combs
#Make new sum(w_list)/3 sets
      if((w+ow)<=g_weight):
        cur_combs.append([w,ow])
#Save sets that are exactly equal to sum(w_list)/3
  for c in cur_combs:
    #print i1,c,sum(c)
    if(sum(c)==g_weight):
      comb_list.append(c)

print comb_list,len(comb_list)
trip_list = []
#Find all combinations of 1/3 weight objects that contain the full set of numbers 
for i1,comb in enumerate(comb_list):
  cur_trips = []
  trip_inds = []
  for i2,comb1 in enumerate(comb_list):
    if(i1!=i2):
      num_count=0
#Add combinations to current triplets
      for i3,c in enumerate(cur_trips):
        n_count=0
        for n in c:
          if(n in comb1):
            n_count+=1
        if(n_count>0):
          continue
        else:
          cur_trips+=[c+comb1]
          #print i2,i3,trip_inds[i3]
          new_ti = trip_inds[i3]+[i2]
          trip_inds+=[new_ti]
        #print 'Add',cur_trips,trip_inds,len(cur_trips),len(trip_inds)
#Create new triplets
      for num in comb:
        if(num in comb1):
          num_count+=1
      if(num_count>0):
        continue
      else:
        cur_trips+=[comb+comb1]
        trip_inds.append([i1,i2])
        #print 'New',cur_trips,trip_inds,len(cur_trips),len(trip_inds)
#Check if list contains all members of w_list
  for inds,ct in enumerate(cur_trips):
    if(len(ct)==len(w_list) and sum(ct)==sum(w_list)):
      #print ct,trip_inds[inds]
      trip_list.append(trip_inds[inds])
count = 0

#Determine the lowest quantum entanglement for the configurations with the fewest packages
min_qe=numpy.inf
min_len=numpy.inf
for l in trip_list:
  count+=1
  qe_val=numpy.inf
  for ind in l:
    cur_qe = reduce(lambda x, y: x*y, comb_list[ind])
    cur_len = len(comb_list[ind])
    if(cur_len<min_len):
      #print cur_len,cur_qe,comb_list[ind]
      min_len=cur_len
      qe_val=cur_qe
  if(qe_val<min_qe):
    min_qe=qe_val

print min_qe 
