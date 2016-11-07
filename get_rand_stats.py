import numpy,sys,random
'''Class that creates a list of random numbers between 0-1, then uses its get_stats method to find the index of the value in the list that is closest to the inut. Once the index is found, it calculates the std dev and mean of the list up to that index'''
class fizz_rnd_list(object):
  def __init__(self,N):
    '''Create the list once. To reduce the complexity of get_stats() from O(n)
        to O(log(n)), sort the list once on instantiation'''
    self.rand_list = [random.random() for i in xrange(0,N)]
    self.rand_list.sort()
  def __str__(self):
    '''Print a list of the numbers in self.rand_list'''
    out_str = '['
    for i in self.rand_list:
      out_str+=str(i)+', '
    if(len(out_str)>1):
      out_str = out_str[:-2]
    out_str+=']'
    return out_str 
  def get_stats(self,X):
  '''Use a binary tree to find the input value in the sorted list. 
     By keeping only the half of the list that contains the number closest 
     to X, only log(n) calls are necessary'''
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
    '''A way of calculating the standard deviation that is easy to implement,
       but definitely not the most efficient. TODO: Make algorithms for std.
       dev. and mean that use dynamic programming to more efficiently calculate
       the result if it is run multiple times'''
    new_list = self.rand_list[:cur_index+1]
    ind_std = numpy.std(new_list)
    ind_mean = numpy.mean(new_list)
    return close_val,cur_index,ind_mean,ind_std           

'''Implement the initial not particularly efficient algorithm for calculating
 all the parameters. Plan to make a dynamic programming algorithm to make the
 std dev and mean calculations more efficient later '''
def main():
  n_iters = int(sys.argv[1])
  my_rand_list = fizz_rnd_list(n_iters)
  for it in xrange(0,n_iters): 
    cur_stat = random.random()
    val,ind,mean,std_dev = my_rand_list.get_stats(cur_stat) 

if __name__=="__main__":
  main()
