import sys
import copy
from copy import deepcopy
r_list = [{'speed':8,'m_time':8,'res_time':53,'r_dist':0,'r_base':0,'r_time':0},
{'speed':13,'m_time':4,'res_time':49,'r_dist':0,'r_base':0,'r_time':0},
{'speed':20,'m_time':7,'res_time':132,'r_dist':0,'r_base':0,'r_time':0},
{'speed':12,'m_time':4,'res_time':43,'r_dist':0,'r_base':0,'r_time':0},
{'speed':9,'m_time':5,'res_time':38,'r_dist':0,'r_base':0,'r_time':0},
{'speed':10,'m_time':4,'res_time':37,'r_dist':0,'r_base':0,'r_time':0},
{'speed':3,'m_time':37,'res_time':76,'r_dist':0,'r_base':0,'r_time':0},
{'speed':9,'m_time':12,'res_time':97,'r_dist':0,'r_base':0,'r_time':0},
{'speed':37,'m_time':1,'res_time':36,'r_dist':0,'r_base':0,'r_time':0}]

#r_list=[{'speed':14,'m_time':10,'res_time':127,'r_dist':0,'r_base':0,'r_time':0},
#{'speed':16,'m_time':11,'res_time':162,'r_dist':0,'r_base':0,'r_time':0}]
r_time = int(sys.argv[1])

def TrackDeer(in_dict1,in_time):
  for i in xrange(1,in_time+1):
    DistCalc(in_dict1)

def DistCalc(in_dict):
  in_dict['r_time']+=1
  if(in_dict['r_time']==in_dict['m_time']):
    in_dict['r_base']+=(in_dict['m_time']*in_dict['speed']) 
    in_dict['r_dist']=in_dict['r_base']
  elif(in_dict['r_time']<in_dict['m_time']):
    in_dict['r_dist']=in_dict['r_base']+(in_dict['r_time']*in_dict['speed'])  
  if(in_dict['r_time']==in_dict['m_time']+in_dict['res_time']):
    in_dict['r_time']=0

score = [0 for i in r_list]
for i_time in xrange(1,r_time+1):
  n_list = deepcopy(r_list)
  win_list = []
  for rdeer in n_list:
    TrackDeer(rdeer,i_time)
    win_list.append(rdeer['r_dist'])
  winner = max(win_list)
  if(len([i for i in win_list if(i==winner)])==1):
    win_ind=win_list.index(winner)
    score[win_ind]+=1
  else:
    for ind,val in enumerate(win_list):
      if(val==winner):
        score[ind]+=1
  #print score,winner,win_list,i_time
print score 
