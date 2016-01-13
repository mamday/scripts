import numpy,math
import sys,os

in_file = sys.argv[1]
ins_list = []
for line in open(in_file).readlines():
  ins_list.append(line.split())

val_dict = {'a':1,'b':0}

print 'List',ins_list,len(ins_list)
cur_ind=0
while(cur_ind<(len(ins_list))):
  print 'Track',val_dict,cur_ind,ins_list[cur_ind]
  if('hlf' in ins_list[cur_ind]):
    print 'Hlf',cur_ind,ins_list[cur_ind],ins_list[cur_ind][1]
    val_dict[ins_list[cur_ind][1]]=val_dict[ins_list[cur_ind][1]]/2
    cur_ind+=1
  elif('tpl' in ins_list[cur_ind]):
    print 'TPL',cur_ind,ins_list[cur_ind],ins_list[cur_ind][1]
    val_dict[ins_list[cur_ind][1]]=3*val_dict[ins_list[cur_ind][1]]
    cur_ind+=1
  elif('inc' in ins_list[cur_ind]):
    print 'Inc',cur_ind,ins_list[cur_ind],ins_list[cur_ind][1]
    val_dict[ins_list[cur_ind][1]]=val_dict[ins_list[cur_ind][1]]+1
    cur_ind+=1
  elif('jie' in ins_list[cur_ind]):
    if(val_dict[ins_list[cur_ind][1][0]]%2==0):
      print 'JIE',cur_ind,ins_list[cur_ind],ins_list[cur_ind][1][0],ins_list[cur_ind][2][1:]
      if(ins_list[cur_ind][2][0]=='+'):
        cur_ind+=int(ins_list[cur_ind][2][1:])
      else:
        cur_ind-=int(ins_list[cur_ind][2][1:])
    else:
      cur_ind+=1
  elif('jio' in ins_list[cur_ind]):
    if(val_dict[ins_list[cur_ind][1][0]]==1):
      print 'JIO',cur_ind,ins_list[cur_ind],ins_list[cur_ind][1][0],ins_list[cur_ind][2][1:]
      if(ins_list[cur_ind][2][0]=='+'):
        cur_ind+=int(ins_list[cur_ind][2][1:])
      else:
        cur_ind-=int(ins_list[cur_ind][2][1:])
    else:
      cur_ind+=1
  else:
    print 'Jump',cur_ind,ins_list[cur_ind][0],ins_list[cur_ind][1][1:]
    if(ins_list[cur_ind][1][0]=='+'):
      cur_ind+=int(ins_list[cur_ind][1][1:])
    else:
      cur_ind-=int(ins_list[cur_ind][1][1:])

print val_dict 
