#include <time.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <algorithm>
#include <cassert>
#include "get_rand_stats.h"

//Initialize int_rnd_list, using the constructor from fizz_rnd_list that takes
// an integer. By using the overloaded constructor, I avoid making an 
// unnecessary extra initialization of fizz_rnd_list
int_rnd_list::int_rnd_list(int N):fizz_rnd_list(N){

}

//Destruct int_rnd_list
int_rnd_list::~int_rnd_list(){

}

//Initialize fizz_rnd_list if the input array length, N, is a float
fizz_rnd_list::fizz_rnd_list(float N): cur_N__(static_cast<int>(N)),x_mean__(0),max_mean_ind__(0){
  int int_N = static_cast<int>(N);
  random_list__ = new double[int_N]();
  //Initialize the maps and the random list once when the class is initiated to
  //avoid spending time looking through the maps for a key later
  for(int i=0; i<int_N; ++i){
    mean_map__[i]=0;
    std_dev_map__[i]=0;
    random_list__[i]=((float)rand()/(float)(RAND_MAX));
  }
  //Sort the algorithm on initialization so that subsequent calls to get_stats
  // can be O(log(n)) instead of O(n)
  std::sort(&random_list__[0],&random_list__[int_N]);
  //TODO: Delete this
  //for(int i=0; i<int_N; ++i){
  //  std::cout<<random_list__[i]<<std::endl;
  //}
}

//Initialize fizz_rnd_list if the input array length, N, is an int
fizz_rnd_list::fizz_rnd_list(int N): cur_N__(N), x_mean__(0), max_mean_ind__(0){
  random_list__ = new double[N]();
  //Initialize the maps and the random list once when the class is initiated to
  //avoid spending time looking through the maps for a key later
  for(int i=0; i<N; ++i){
    mean_map__[i]=0;
    std_dev_map__[i]=0;
    random_list__[i]=rand() % 1000;
  }
  //Sort the algorithm on initialization so that subsequent calls to get_stats
  // can be O(log(n)) instead of O(n)
  std::sort(&random_list__[0],&random_list__[N]);
  //TODO: Delete this
  //for(int i=0; i<N; ++i){
  //  std::cout<<random_list__[i]<<std::endl;
  //}
}

//Destruct fizz_rnd_list, making sure to abolish the dynamically allocated array
fizz_rnd_list::~fizz_rnd_list(){
  delete [] random_list__;
}

double* fizz_rnd_list::get_list(){
  return random_list__;
}

double fizz_rnd_list::get_mean(int X_ind){
  double cur_tot = 0;
  //If the value already exists, don't calculate it again. This is much more
  //efficient than calculating the mean for the same list multiple times when
  //it has already been calculated before
  if(mean_map__[X_ind]!=0){
    return mean_map__[X_ind];
  }
  //If the current index is greater than the previous highest index, get the
  //start calculating the mean at the previous highest index
  if(X_ind>max_mean_ind__){
    cur_tot = max_mean_ind__*mean_map__[max_mean_ind__];
  } 

  //Calculate the mean continuously and save the value up to the current index
  for(int i=max_mean_ind__; i<(X_ind); ++i){
    cur_tot+=random_list__[i]; 
    mean_map__[i+1]=cur_tot/(i+1);
  }

  //If the current index is higher than the previous index, replace it as the
  //maximum index
  if(X_ind>max_mean_ind__){
    max_mean_ind__=X_ind;
  }

  return cur_tot/(float)(X_ind);
}

double fizz_rnd_list::get_std_dev(int X_ind){
  double cur_tot = 0;
  //If the standard deviation has already been calculated, don't calculate it 
  //again, to be more efficient.
  if(std_dev_map__[X_ind]!=0){
    return std_dev_map__[X_ind];
  }
  //Otherwise calculate the stardard deviation from the current value of the mean
  for(int i=0; i<(X_ind); ++i){
    cur_tot+=(random_list__[i]-mean_map__[X_ind])*(random_list__[i]-mean_map__[X_ind]); 
  }
  //Save the current value in the map
  std_dev_map__[X_ind]=sqrt(cur_tot/(float)(X_ind));

  return sqrt(cur_tot/(float)(X_ind));
}

double fizz_rnd_list::get_uniform_std_dev(int X_ind){
  return sqrt((((float)(X_ind-1)/float(cur_N__))*((float)(X_ind-1)/float(cur_N__)))/12); 
}

//Return stats as tuple with 1)Value closes to X 2)Index of Value 3)Mean up to
//Index and 4)Std. Dev up to Index
std::tuple<double, int, double, double> fizz_rnd_list::get_stats(double X){
  //Fail if there are no entries in the array
  if(cur_N__==0){
    std::cerr<<"ERROR: Random array has no entries"<<std::endl;
    exit(EXIT_FAILURE);
  } 
  int cur_index = -1;
  double close_val = -1;
  int cur_len = cur_N__; 
  double* cur_list = random_list__;
  while(cur_len>1){
    //In order to quickly access the halves, instead of copying from the 
    // original array I just make pointers to certain parts of the array 
    double *firstHalf = &cur_list[0];
    double *secondHalf = &cur_list[(cur_len/2)];
    //Use a binary tree in order to keep only looking in parts of the list
    //that contain the final value, so the algorithm will be O(log(n)) and 
    // not O(n)
    if(firstHalf[(cur_len/2)-1]==secondHalf[0]){
      //If the values in the middle of the list are equal, move to the low 
      //values if the difference between the input and the middle value is 
      //negative. This is because, if the value is negative, then that means the
      //middle value is greater than the input value, so therefore we should 
      //take the list containing smaller values (the left branch'''
      if((X-firstHalf[(cur_len/2)-1])<=0){

        if(cur_len==cur_N__){
          cur_index = 0;
        }
        cur_len = (cur_len/2);
        cur_list = firstHalf;

      }
      else{
        if(cur_len==cur_N__){
          cur_index = cur_len/2;
        }
        else{
          cur_index = cur_index + (cur_len/2);
        }
        cur_len = ceil((float)cur_len/2.0);
        cur_list = secondHalf;

      }

    }
    //If the values are not equal, go in the direction that is closer to the 
    //input value X
    else if(std::abs(firstHalf[(cur_len/2)-1]-X)<=std::abs(secondHalf[0]-X)){
      if(cur_len==cur_N__){
        cur_index = 0;
      }
      cur_len = (cur_len/2);
      cur_list = firstHalf;
    }
    else{
      if(cur_len==cur_N__){
        cur_index = cur_len/2; 
      }
      else{
        cur_index = cur_index + (cur_len/2);
      }
      cur_len = ceil((float)cur_len/2.0);
      cur_list = secondHalf;
    }
    if(cur_len==1){
      close_val=cur_list[0];
    }
  }
  //If the previous value is the same as the current value, look backwards in 
  //the list by halves (splitting the list) until it finds the earliest value
  //that is the same. This fixes the problem where the closest value is smaller
  //than the input value and occurs multiple times. TODO Make a function to 
  //reduce the number of times I use the binary tree logic for calculating the
  // current length and index
  if(cur_index>0 && close_val==random_list__[cur_index-1]){
    double* cur_half = random_list__;
    int cur_len = cur_index+1; 
    int new_index = 0; 
    while(cur_len>1){
      double *firstHalf = &cur_half[0];
      double *secondHalf = &cur_half[cur_len/2];
      if((close_val-firstHalf[(cur_len/2)-1])==0){
        if(cur_len==cur_index+1){
          new_index = 0;
        }
        cur_half=firstHalf;
        cur_len = (cur_len/2);
      }
      else{
        if(cur_len==cur_index+1){
          new_index = cur_len/2;
        }
        else{
          new_index = new_index + (cur_len/2);
        }
        cur_half=secondHalf;
        cur_len = ceil((float)cur_len/2.0);

      }
    }
    cur_index=new_index;
  }
  //Implement a method for calculating the mean that stores the results for 
  // every index so they don't have to be calculated again
  //Implement a brute force method for calculating the standard deviation
  //using the fact that it is sampled from a uniform distribution. If the
  //length of the random list is >1000 the error is mostly <10%
  double x_mean__=0;
  double std_dev=0;
  if(cur_index==0){
    return std::make_tuple(close_val,cur_index,x_mean__,std_dev);
  }

  x_mean__ = get_mean(cur_index);
  if(cur_N__<1000){
    std_dev = get_std_dev(cur_index);
  }
  else{
    std_dev = get_uniform_std_dev(cur_index);
  }

  return std::make_tuple(close_val,cur_index,x_mean__,std_dev);
}

//Implement my unit test framework
test_rnd_list::test_rnd_list(){
}

test_rnd_list::~test_rnd_list(){
}

//Test that initiation of fizz_rnd_list class produces 10 entries between 0 and
//1
void test_rnd_list::test_fizz_rnd_list_initiation(){
  float l_len = 10;
  fizz_rnd_list test_list(l_len);
  double* test_rand = test_list.get_list();
  int test_len = 0;
  while(test_len<l_len){
    assert(test_rand[test_len]>0 && test_rand[test_len]<1);
    test_len+=1;
  }
}

//Test that initiation of int_rnd_list class produces 10 entries between 0 and 
//1000
void test_rnd_list::test_int_rnd_list_initiation(){
  int l_len = 10;
  int_rnd_list test_list(l_len);
  double* test_rand = test_list.get_list();
  int test_len = 0;
  while(test_len<l_len){
    assert(test_rand[test_len]>0 && test_rand[test_len]<1000);
    test_len+=1;
  }
}

//Test that uniform standard deviation algorithm returns the expected value
//given a uniform distribution
void test_rnd_list::test_uniform_std_dev(){
  int l_len=1000;
  int_rnd_list test_list(l_len);
  double u_std_dev = test_list.get_uniform_std_dev(300);

  assert((u_std_dev-0.0866)<0.0001);
}

//Test that if I create a list with one entry that the mean is that entry
void test_rnd_list::test_get_mean_zero(){
  int_rnd_list test_list(1);
  double* test_rand = test_list.get_list();
  double mean = test_list.get_mean(1);
  assert(mean==test_rand[0]);
}

//Test that if I create a list with one entry that the standard deviation is 
//zero 
void test_rnd_list::test_get_std_dev_zero(){
  int_rnd_list test_list(1);
  double* test_rand = test_list.get_list();
  double mean = test_list.get_mean(1);
  double std_dev = test_list.get_std_dev(1);
  assert(std_dev==0);
}

//Test that if I create a list with two entries that the mean is half of the sum
//of those two entries 
void test_rnd_list::test_get_mean_one(){
  int_rnd_list test_list(2);
  double* test_rand = test_list.get_list();
  double mean = test_list.get_mean(2);
  assert(mean==((test_rand[0]+test_rand[1])/2));
}

//Test that if I create a list with two entries that the standard deviation is 
//the square root of the difference of those two entries from their mean divided//by two 
void test_rnd_list::test_get_std_dev_one(){
  int_rnd_list test_list(2);
  double* test_rand = test_list.get_list();
  double mean = test_list.get_mean(2);
  double std_dev = test_list.get_std_dev(2);
  assert(std_dev==sqrt((((test_rand[0]-mean)*(test_rand[0]-mean))/2)+(((test_rand[1]-mean)*(test_rand[1]-mean))/2))
);
}

//Test that if I create a list with three entries that the mean is a third of
// the sum of those three entries 
void test_rnd_list::test_get_mean_two(){
  int_rnd_list test_list(3);
  double* test_rand = test_list.get_list();
  double mean = test_list.get_mean(3);
  assert(mean==((test_rand[0]+test_rand[1]+test_rand[2])/3));
}

//Test that if I calculate the mean up to index 1, and then calculate the mean 
//up to index two, that the result is the same as if I calculate the mean just
//once up to index two
void test_rnd_list::test_get_mean_repeat(){
  int_rnd_list test_list(2);
  double* test_rand = test_list.get_list();
  double mean = test_list.get_mean(1);
  double mean1 = test_list.get_mean(2);
  assert(mean1==((test_rand[0]+test_rand[1])/2));
}

//Test that if I calculate the mean up to index 1, and then calculate the mean 
//up to index two, and then calculate the mean up to index 3 that the result is
//the same as if I calculate the mean just once up to index three
void test_rnd_list::test_get_mean_threepeat(){
  int_rnd_list test_list(3);
  double* test_rand = test_list.get_list();
  double mean = test_list.get_mean(1);
  double mean1 = test_list.get_mean(2);
  double mean2 = test_list.get_mean(3);
  assert(mean2==((test_rand[0]+test_rand[1]+test_rand[2])/3));
}

//Test that the get_stats algorithm gets the highest value in the list if I give//a number greater than 1 and the lowest number if I give a number lower than 0
void test_rnd_list::test_get_stats_ends(){
  float in_len = 3;
  fizz_rnd_list test_list(in_len);
  double* test_rand = test_list.get_list();

  std::tuple<double, int, double, double> stats = test_list.get_stats(2); 
  assert(std::get<1>(stats)==2 && std::get<0>(stats)==test_rand[2]); 

  std::tuple<double, int, double, double> stats1 = test_list.get_stats(-1); 
  assert(std::get<1>(stats1)==0 && std::get<0>(stats1)==test_rand[0]); 
}
void test_rnd_list::test_get_stats(){
  float in_len = 100000;
  int_rnd_list test_list(in_len);
  int test_val = 500;
  double* test_rand = test_list.get_list();
  std::tuple<double, int, double, double> stats = test_list.get_stats(test_val); 

  int cor_ind =0;
  double cor_val=0;
  double diff=1001;
  for(int i=0; i<in_len; ++i){
    double cur_diff=std::abs(test_val-test_rand[i]);
    if(cur_diff<diff){
      cor_ind=i;
      cor_val=test_rand[i];
      diff=cur_diff;
    }
  }
  assert(std::get<1>(stats)==cor_ind && std::get<0>(stats)==cor_val); 
  
}

// Get the length of the array and the number of times to iterate from the 
// command line (num). Then initialize either int_rnd_list (if the second 
// argument is thousand) or fizz_rnd_list(if the second argument is one).
// The get_stats() function that is shared by both classes will get a tuple
// that contains 1)The closest value close_val, to X (which is randomly generated in the 
// loop and is called 'rand_num') 2)The index of close_val 3)The mean of all
// the values up to the index 4)The standard deviation of all the values up to
// the index 
int main(int argc, char* argv[]){
  //Initialize random number generator
  srand(time(NULL));
  //If one input is given, and the name of the input is 'test', then run the 
  //tests
  if(argc == 2){
    std::string in_string(argv[1]);
    if(in_string!="test"){
      std::cerr<<"ERROR: Received the incorrect number of arguments"<<std::endl;
      exit(EXIT_FAILURE);
    }
    test_rnd_list tester;
    tester.test_fizz_rnd_list_initiation();
    tester.test_int_rnd_list_initiation();
    tester.test_uniform_std_dev();
    tester.test_get_mean_zero();
    tester.test_get_std_dev_zero();
    tester.test_get_mean_one();
    tester.test_get_std_dev_one();
    tester.test_get_mean_two();
    tester.test_get_mean_repeat();
    tester.test_get_mean_threepeat();
    tester.test_get_stats();
    tester.test_get_stats_ends();
    std::cout<<"Passed!"<<std::endl;
  }
  //Exit if the wrong number of inputs are given
  else if(argc != 3){
    std::cerr<<"ERROR: Received the incorrect number of arguments"<<std::endl;
    exit(EXIT_FAILURE);
  } 
  else{
    //Make the input a float so that we get the correct behavior of fizz_rnd_list
    float num = atof(argv[1]);
    //Change the input char array into a string that is easier to parse
    std::string in_string(argv[2]);
    //Execute the get_stats() function for int_rnd_list if in_string is 'thousand'
    // and for fizz_rnd_list if the input is 'one'. Otherwise complain.
    std::tuple<double,int,double,double> fin_tup;
    double rand_num;
    if(in_string=="thousand"){
      int_rnd_list i_rnd(num);
      for(int i=0; i<(num+1); ++i){
        rand_num = rand() % 1000;
        fin_tup = i_rnd.get_stats(rand_num);
        //The following will print the tuple if you want. Could make this a function
        //std::cout<<rand_num<<" "<<std::get<0>(fin_tup)<<" "<<std::get<1>(fin_tup)<<" "<<std::get<2>(fin_tup)<<" "<<std::get<3>(fin_tup)<<std::endl;
      }
    }
    else if(in_string=="one"){
      fizz_rnd_list f_rnd(num);
      for(int i=0; i<(num+1); ++i){
        rand_num = (float)rand()/(float)(RAND_MAX);
        fin_tup = f_rnd.get_stats(rand_num); 
        //The following will print the tuple if you want. Could make this a function
        //std::cout<<rand_num<<" "<<std::get<0>(fin_tup)<<" "<<std::get<1>(fin_tup)<<" "<<std::get<2>(fin_tup)<<" "<<std::get<3>(fin_tup)<<std::endl;
      }
    }
    else{
      //Fail if the input is not 'one' or 'thousand'
      std::cerr<<"ERROR: Invalid algorithm classifier"<<std::endl;
      exit(EXIT_FAILURE);
    }
  }
}

