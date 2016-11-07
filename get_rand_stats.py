import numpy,sys,random

class fizz_rnd_list(object):
  def __init__(self,N):
    self.rand_list = [random.random() for i in xrange(0,N)]
    self.rand_list.sort()
  def __str__(self):
    out_str = '['
    for i in self.rand_list:
      out_str+=str(i)+', '
    if(len(out_str)>1):
      out_str = out_str[:-2]
    out_str+=']'
    return out_str 
  def get_stats(self,X):
    cur_index = -1
    close_val = -1
    if(len(self.rand_list)==0):
      raise Exception('Random list contains no values')
    r_nums = self.rand_list
    while(len(r_nums)>1):
      low_nums = r_nums[:(len(r_nums)/2)]
      high_nums = r_nums[(len(r_nums)/2):]
      if(abs(low_nums[-1]-X)<abs(high_nums[0]-X)):
        if(cur_index==-1):
          cur_index = 0 
        else:
          pass  
        r_nums = low_nums
      else:
        if(cur_index==-1):
          cur_index = len(r_nums)/2 
        else:
          cur_index = cur_index + len(r_nums)/2 
        r_nums = high_nums
      if(len(r_nums)==1):
        close_val=r_nums[0]
    return close_val,cur_index           

  #def update_std(self,cur_M):

  #def update_mean(self,cur_M):


