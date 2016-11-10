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
    self.max_mean_dict_ind = 0 

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

    if(ind>self.max_mean_dict_ind):
      cur_tot = (self.max_mean_dict_ind)*self.mean_dict[self.max_mean_dict_ind] 

    for i in xrange(self.max_mean_dict_ind,ind):
       cur_tot+=self.rand_list[i]
       self.mean_dict[i+1]=cur_tot/(i+1)

    if((ind)>self.max_mean_dict_ind):
      self.max_mean_dict_ind=ind

    return cur_tot/(ind)

  '''This version of calculating the standard deviation saves the result if an 
  index has already been calculated, similar to the implementation for 
  get_mean(). However, since the mean of the distribution will be different for
  different indices, it does not save the results as it calculates them.'''
  def get_std_dev(self,ind):
    if(not(ind in self.mean_dict)):
      raise Exception('Must calculate mean before calculating standard deviation')
    cur_tot=0.0
    if(ind in self.std_dev_dict):
      return self.std_dev_dict[ind]

    var_array = (numpy.array(self.rand_list[:ind])-self.mean_dict[ind])*(numpy.array(self.rand_list[:ind])-self.mean_dict[ind])
    cur_tot= sum(var_array)

    self.std_dev_dict[ind]=numpy.sqrt(cur_tot/(ind))

    return self.std_dev_dict[ind] 

  '''Function that just returns the expected standard deviation of a uniform 
  distribution between 0 and the index before the selected index'''
  def get_uniform_std_dev(self,ind):

    return numpy.sqrt(((float(ind-1)/float(len(self.rand_list)))**2)/12.)

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
      '''If the values in the middle of the list are equal, move to the low 
      values if the difference between the input and the middle value is 
      negative. This is because, if the value is negative, then that means the
      middle value is greater than the input value, so therefore we should take
      the list containing smaller values (the left branch'''
      if(low_nums[-1]==high_nums[0]):

        if((X-low_nums[-1])<0):
          if(cur_index==-1):
            cur_index = 0
          r_nums = low_nums

        else:

          if(cur_index==-1):
            cur_index = len(r_nums)/2
          else:
            cur_index = cur_index + len(r_nums)/2
          r_nums = high_nums
      '''If the values are not equal, go in the direction that is closer to the
      input value X'''
      elif(abs(low_nums[-1]-X)<abs(high_nums[0]-X)):

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

    '''Implemented a new method for calculating the mean that stores previous
    results so that multiple calls are more efficient. Find that using the 
    numpy method to calculate the standard deviation is more efficient than
    trying to calculate the standard deviation manually. Storing the results in
    a dictionary also only marginally improves the speed for large N'''
    new_list = self.rand_list[:cur_index+1]
    ind_mean = self.get_mean(cur_index)
    '''If you are willing to accept some error (<10% for N>1000) you can quickly
    calculate the standard deviation from the index, since the distribution 
    is uniform'''
    ind_std=0
    if(len(self.rand_list)<1000):

      if(not(cur_index in self.std_dev_dict)):
        ind_std = numpy.std(new_list)
      else:
        ind_std = self.std_dev_dict[cur_index]

    else:
      ind_std = self.get_uniform_std_dev(cur_index)

    return close_val,cur_index,ind_mean,ind_std           

'''Implement the efficient algorithm for calculating the value and index of
the entry in the n_iters long list of random numbers that is closest to 
cur_stat. Then calculate the mean and standard deviation up to the index.''' 
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

'''Test that implementing the fizz_rnd_list class creates a list of random 
numbers that has a length equal to the input'''
def test_fizz_rnd_list_initiation():
  l_len = 10
  test_list = fizz_rnd_list(l_len)
  assert(isinstance(test_list.rand_list,list) and len(test_list.rand_list)==10)

'''Test the algorithm that calculates the standard deviation using the 
approximation for a uniform distribution'''
def test_uniform_std_dev():
  test_list = fizz_rnd_list(1000)
  test_rand = test_list.rand_list
  mean = test_list.get_mean(1000)
  u_std_dev = test_list.get_uniform_std_dev(300)
  assert (u_std_dev-numpy.std(test_rand[:300]))/(numpy.std(test_rand[:300]))<0.1  

'''Test that if I create a list with one entry that the mean is that entry'''
def test_get_mean_zero():
  test_list = fizz_rnd_list(1)
  test_rand = test_list.rand_list
  mean = test_list.get_mean(1)
  assert mean==test_rand[0]

'''Test that if I create a list with one entry that the standard deviation is 
zero.'''
def test_get_std_dev_zero():
  test_list = fizz_rnd_list(1)
  test_rand = test_list.rand_list
  mean = test_list.get_mean(1)
  std_dev = test_list.get_std_dev(1)
  assert std_dev==0

'''Test that if I create a list with two entries that the mean is the sum of 
those entries divided by two'''
def test_get_mean_one():
  test_list = fizz_rnd_list(2)
  test_rand = test_list.rand_list
  mean = test_list.get_mean(2)
  assert mean==((test_rand[0]+test_rand[1])/2)

'''Test that if I create a list with two entries that the standard deviation is
the square root of the difference of those two entries from their mean divided 
by two.'''
def test_get_std_dev_one():
  test_list = fizz_rnd_list(2)
  test_rand = test_list.rand_list
  mean = test_list.get_mean(2)
  std_dev = test_list.get_std_dev(2)
  assert std_dev==numpy.sqrt((((test_rand[0]-mean)*(test_rand[0]-mean))/2)+(((test_rand[1]-mean)*(test_rand[1]-mean))/2))

'''Test that if I create a list with three entries that the mean is the sum of 
those entries divided by three'''
def test_get_mean_two():
  test_list = fizz_rnd_list(3)
  test_rand = test_list.rand_list
  mean = test_list.get_mean(3)

  assert mean==((test_rand[0]+test_rand[1]+test_rand[2])/3)


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

'''Test that get_stats gets the correct index and value in the list, and then
gets the mean and standard deviation'''
def test_get_stats():
  test_list = fizz_rnd_list(3)
  test_rand = test_list.rand_list
  test_val = 0.4
  val,ind,mean,std_dev = test_list.get_stats(test_val)
  cor_ind_val = min(enumerate(abs(numpy.array(test_rand)-test_val)),key=lambda x: x[1]) 
  cor_ind = cor_ind_val[0]
  cor_val = test_rand[cor_ind] 
  if(cor_ind>0):
    cor_mean = numpy.mean(test_rand[:cor_ind])
    cor_std = numpy.std(test_rand[:cor_ind+1])
  else:
    cor_mean=0
    cor_std=0
  assert(ind==cor_ind and val==cor_val and mean==cor_mean and std_dev==cor_std)
