import sys
import copy
from copy import deepcopy

in_file = sys.argv[1]
hap_dict = {} 
n_keys = []
for line in open(in_file).readlines():
  info = line.split(' ')
  if(not str(info[0]) in n_keys):
    n_keys.append(str(info[0]))
  if(not str(info[10][:-2]) in n_keys):
    n_keys.append(str(info[10][:-2]))
  if('gain' in info):
    hap_dict[(str(info[0]),str(info[10][:-2]))]=int(info[3])
  elif('lose' in info):
    hap_dict[(str(info[0]),str(info[10][:-2]))]=-1*int(info[3])

def TestNode(name_key):
  in_score = hap_dict[name_key]
  cur_score = 0 
  node = ()
  c_keys = [name_key[0],name_key[1]]
  name_dict = {key: val for key,val in hap_dict.iteritems() if(key[0]==name_key[0]) and (not(key[1] in c_keys))}
  for names,score in name_dict.iteritems():
    if((in_score+score)>cur_score):
      cur_score = in_score
      node=names

