#include <time.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <algorithm>
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
fizz_rnd_list::fizz_rnd_list(float N): cur_N(static_cast<int>(N)),x_mean(0){
  int int_N = static_cast<int>(N);
  random_list__ = new double[int_N]();
  for(int i=0; i<int_N; ++i){
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
fizz_rnd_list::fizz_rnd_list(int N): cur_N(N), x_mean(0){
  random_list__ = new double[N]();
  for(int i=0; i<N; ++i){
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

double fizz_rnd_list::get_mean(int X_ind){
  double cur_tot = 0;
  //This is just a standard algorithm to loop through the indices and calculate
  // the mean. It is not very efficient right now. TODO
  for(int i=0; i<(X_ind+1); ++i){
    cur_tot+=random_list__[i]; 
  }
  return cur_tot/(float)(X_ind+1);
}

double fizz_rnd_list::get_std_dev(int X_ind){
  double cur_tot = 0;
  //This is just a standard algorithm to loop through the indices and calculate
  // the standard deviation. It is not very efficient right now. TODO
  for(int i=0; i<(X_ind+1); ++i){
    cur_tot+=(random_list__[i]-x_mean)*(random_list__[i]-x_mean); 
  }
  return sqrt(cur_tot/(float)(X_ind+1));
}

std::tuple<double, int, double, double> fizz_rnd_list::get_stats(double X){
  //Fail if there are no entries in the array
  if(cur_N==0){
    std::cerr<<"ERROR: Random array has no entries"<<std::endl;
    exit(EXIT_FAILURE);
  } 
  int cur_index = -1;
  double close_val = -1;
  int cur_len = cur_N; 
  double* cur_list = random_list__;
  while(cur_len>1){
    //In order to quickly access the halves, instead of copying from the 
    // original array I just make pointers to certain parts of the array 
    double *firstHalf = &cur_list[0];
    double *secondHalf = &cur_list[cur_len/2];
    //Use a binary tree in order to keep only looking in parts of the list
    //that contain the final value, so the algorithm will be O(log(n)) and 
    // not O(n)
    if(std::abs(firstHalf[(cur_len/2)-1]-X)<std::abs(secondHalf[0]-X)){
      if(cur_len==cur_N){
        cur_index = 0;
      }
      cur_len = (cur_len/2);
      cur_list = firstHalf;
    }
    else{
      if(cur_len==cur_N){
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
  //Use my very inefficient methods for calculating the mean and the standard
  // deviation for now
  x_mean = get_mean(cur_index);
  double std_dev = get_std_dev(cur_index);

  return std::make_tuple(close_val,cur_index,x_mean,std_dev);
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
  //Exit if the wrong number of inputs are given
  if(argc != 3){
    std::cerr<<"ERROR: Received the incorrect number of arguments"<<std::endl;
    exit(EXIT_FAILURE);
  } 
  //Make the input a float so that we get the correct behavior of fizz_rnd_list
  float num = atof(argv[1]);
  //Change the input char array into a string that is easier to parse
  std::string in_string(argv[2]);
  //Execute the get_stats() function for int_rnd_list if in_string is 'thousand'
  // and for fizz_rnd_list if the input is 'one'. Otherwise complain.
  std::tuple<double,int,double,double> fin_tup;
  double rand_num;
  if(in_string=="thousand"){
    for(int i=0; i<(num+1); ++i){
      int_rnd_list i_rnd(num);
      rand_num = rand() % 1000;
      fin_tup = i_rnd.get_stats(rand_num);
      //The following will print the tuple if you want. Could make this a function
      std::cout<<rand_num<<" "<<std::get<0>(fin_tup)<<" "<<std::get<1>(fin_tup)<<" "<<std::get<2>(fin_tup)<<" "<<std::get<3>(fin_tup)<<std::endl;
    }
  }
  else if(in_string=="one"){
    for(int i=0; i<(num+1); ++i){
      fizz_rnd_list f_rnd(num);
      rand_num = (float)rand()/(float)(RAND_MAX);
      fin_tup = f_rnd.get_stats(rand_num); 
      //The following will print the tuple if you want. Could make this a function
      std::cout<<rand_num<<" "<<std::get<0>(fin_tup)<<" "<<std::get<1>(fin_tup)<<" "<<std::get<2>(fin_tup)<<" "<<std::get<3>(fin_tup)<<std::endl;
    }
  }
  else{
    //Fail if the input is not 'one' or 'thousand'
    std::cerr<<"ERROR: Invalid algorithm classifier"<<std::endl;
    exit(EXIT_FAILURE);
  }

}

