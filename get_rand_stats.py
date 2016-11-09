import numpy,sys,random
'''Class that creates a list of random numbers between 0-1, then uses its 
get_stats method to find the index of the value in the list that is closest
to the input. Once the index is found, it calculates the std dev and mean
of the list up to that index'''
class fizz_rnd_list(object):
  def __init__(self,N):
    '''Create the list once. To reduce the complexity of get_stats() from O(n)
        to O(log(n)), sort the list once on instantiation'''
    self.rand_list = [random.random() for i in xrange(0,N)]
    self.rand_list.sort()
    self.mean_dict = {0:0}
    self.std_dev_dict = {0:0}
    self.max_dict_ind = 0 
  def __str__(self):
    '''Print a list of the numbers in self.rand_list'''
    out_str = '['
    for i in self.rand_list:
      out_str+=str(i)+', '
    if(len(out_str)>1):
      out_str = out_str[:-2]
    out_str+=']'
    return out_str 
  '''This version of calculating the mean saves the result if an index has
  already been calculated. If the index is greater than the maximum index
  that was ever calculated, it starts from the maximum index value and only
  iterates until it gets to to the current index. This saves time, and is 
  most efficient, because the mean does not have to be calculated multiple 
  times for the same index, and takes fewer iterations to calculate the more
  you run the algorithm'''
  def get_mean(self,ind):
    cur_tot=0.0
    if(ind in self.mean_dict):
      return self.mean_dict[ind]

    if(ind>self.max_dict_ind):
      cur_tot = (self.max_dict_ind)*self.mean_dict[self.max_dict_ind] 

    for i in xrange(self.max_dict_ind,ind):
       cur_tot+=self.rand_list[i]
       self.mean_dict[i+1]=cur_tot/(i+1)

    if((ind)>self.max_dict_ind):
      self.max_dict_ind=ind

    return cur_tot/(ind)

  def get_stats(self,X):
    '''Use a binary tree to find the input value in the sorted list. 
    By keeping only the half of the list that contains the number closest 
    to X, only log(n) calls are necessary'''
    cur_index = -1
    close_val = -1
    '''Raise an exception if the list is empty'''
    if(len(self.rand_list)==0):
      raise Exception('Random list contains no values')
    r_nums = self.rand_list
    while(len(r_nums)>1):
      low_nums = r_nums[:(len(r_nums)/2)]
      high_nums = r_nums[(len(r_nums)/2):]
      if(abs(low_nums[0]-X)<abs(high_nums[-1]-X)):
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
    ind_mean = self.get_mean(cur_index)
    return close_val,cur_index,ind_mean,ind_std           

'''Implement the efficient algorithm for calculating the value and index of
the entry in the n_iters long list of random numbers that is closest to 
cur_stat. Method for calculating mean and standard deviation is currently 
not very efficent. Plan to make a dynamic programming algorithm to make the
std dev and mean calculations more efficient later '''
def main():
  n_iters = int(sys.argv[1])
  my_rand_list = fizz_rnd_list(n_iters)
  for it in xrange(0,n_iters): 
    cur_stat = random.random()
    val,ind,mean,std_dev = my_rand_list.get_stats(cur_stat) 
    #A simple way to output the result, if you want
    #print cur_stat,val,ind,mean,std_dev

if __name__=="__main__":
  main()

'''Tests that can be run with python -m pytest get_rand_stats.py'''

'''Test that if I create a list with one entry that the mean is that entry'''
def test_get_mean_zero():
  test_list = fizz_rnd_list(1)
  test_rand = test_list.rand_list
  mean = test_list.get_mean(1)
  assert mean==test_rand[0]

'''Test that if I create a list with two entries that the mean is the sum of 
those entries divided by two'''
def test_get_mean_one():
  test_list = fizz_rnd_list(2)
  test_rand = test_list.rand_list
  mean = test_list.get_mean(2)
  assert mean==((test_rand[0]+test_rand[1])/2)

'''Test that if I create a list with three entries that the mean is the sum of 
those entries divided by three'''
def test_get_mean_two():
  test_list = fizz_rnd_list(3)
  test_rand = test_list.rand_list
  mean = test_list.get_mean(3)

'''Test that if I calculate the mean up to index 1, and then calculate the mean 
up to index two, that the result is the same as if I calculate the mean just
nce up to index two'''
def test_get_mean_repeat():
  test_list = fizz_rnd_list(2)
  test_rand = test_list.rand_list
  mean = test_list.get_mean(1)
  mean1 = test_list.get_mean(2)
  assert mean1==((test_rand[0]+test_rand[1])/2)

'''Test that if I calculate the mean up to index 1, and then calculate the mean 
up to index two, and then calculate the mean up to index 3 that the result is the same as if I calculate the mean just once up to index three'''
def test_get_mean_threepeat():
  test_list = fizz_rnd_list(3)
  test_rand = test_list.rand_list
  mean = test_list.get_mean(1)
  mean1 = test_list.get_mean(2)
  mean2 = test_list.get_mean(3)
  assert mean2==((test_rand[0]+test_rand[1] + test_rand[2])/3)


