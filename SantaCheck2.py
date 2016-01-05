import numpy
import sys
import copy
in_file=sys.argv[1]

def testStr(in_str):
    pair_list = []
    cur_pair=''
    s_count=0
    doub_count=0
    for i in in_str:
        print i,cur_pair,pair_list,s_count,doub_count
        if(len(cur_pair)<2):
            cur_pair = cur_pair+i
        else:
          pair_list.append(cur_pair)
          if(i==cur_pair[0]):
              s_count+=1
          cur_pair = cur_pair[1:]+i
          if((not(cur_pair==pair_list[-1]) or (len(pair_list)>1 and (cur_pair==pair_list[-2]))) and (cur_pair in pair_list)):
              doub_count+=1
    if(s_count>0 and doub_count>0):
      return 'Good'
g_count=0
for line in open(in_file).readlines():
    g_val = testStr(str(line))
    if(g_val=='Good'):
        g_count+=1
    print g_val
print g_count