import numpy
import sys
in_file=sys.argv[1]

def testStr(in_str):
  if(('ab' in in_str) or ('cd' in in_str) or ('pq' in in_str) or ('xy' in in_str)):
    return
  v_count=0
  v_str='aeiou'
  double_count=0
  prev_str=''
  for i in in_str:
    if(i in v_str):
      v_count+=1
    
    if(i==prev_str):
      double_count+=1
    prev_str=i
  if(v_count>2 and double_count>0):
    return 'Good'
gCount=0
for line in open(in_file).readlines():  
  g_val = testStr(str(line))
  if(g_val=='Good'):
    gCount+=1
print gCount