import sys,os
import copy
from copy import deepcopy

in_file = sys.argv[1]
eggnog = int(sys.argv[2])

conts = []
for line in open(in_file).readlines():
  conts.append(int(line))

global d_track,comb_list 
comb_list = {} 

def ContTest(cont,cur_conts):
  print 'Every',cur_conts
  global dtrack,comb_list
  for cont1 in conts:
   # print 'Beg',cont,cont1,d_track
    if(not(cont1 in d_track)):
      print 'Cont'
      continue
    print 'Start',cont,cont1,d_track,cur_conts,conts.count(cont1),sum(cur_conts),comb_list
    d_track.remove(cont1)
    cur_conts.append(cont1)
    if((eggnog-(sum(cur_conts)))>=0):
      if((eggnog-(sum(cur_conts)))==0):
        print 'B',cont,cont1,d_track,deepcopy(cur_conts)
        c_list = deepcopy(cur_conts) 
        c_list.sort()
        comb_list[tuple(c_list)]=1
        cur_conts = cur_conts[:-1]
        print 'A',cont,cont1,d_track,deepcopy(cur_conts)
      else:
        ContTest(cont1,cur_conts)
        print 'RecB',cont,cont1,d_track,cur_conts
        cur_conts = cur_conts[:-1]
        print 'RecA',cont,cont1,d_track,cur_conts
        d_track.append(cont1)
    else:
      print 'End',cont,cont1,d_track,cur_conts
      cur_conts = cur_conts[:-1] 

for cont0 in conts:
  cur_conts1 = []
  cur_conts1.append(cont0)
  d_track = deepcopy(conts) 
  d_track.remove(cont0)
  ContTest(cont0,cur_conts1)

tot_count = 0
for comb,val in comb_list.iteritems():
  d_count = 0
  for con in comb:
    if(conts.count(con)>1):
      d_count+=(conts.count(con)-comb.count(con))
  tot_count+=val*(2**d_count)
  print comb,val*(2**d_count)

print tot_count 
