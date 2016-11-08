#include <time.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <algorithm>
#include "get_rand_stats.h"

int_rnd_list::int_rnd_list(int N):fizz_rnd_list(N){

}

int_rnd_list::~int_rnd_list(){

}

fizz_rnd_list::fizz_rnd_list(float N): cur_N(static_cast<int>(N)),x_mean(0){
  int int_N = static_cast<int>(N);
  random_list__ = new double[int_N]();
  srand((unsigned int) time(NULL));
  for(int i=0; i<int_N; ++i){
    random_list__[i]=((float)rand()/(float)(RAND_MAX));
  }
  std::sort(&random_list__[0],&random_list__[int_N]);
  for(int i=0; i<int_N; ++i){
    std::cout<<random_list__[i]<<std::endl;
  }
}

fizz_rnd_list::fizz_rnd_list(int N): cur_N(N), x_mean(0){
  random_list__ = new double[N]();
  srand((unsigned int) time(NULL));
  for(int i=0; i<N; ++i){
    random_list__[i]=rand() % 1000;
  }
  std::sort(&random_list__[0],&random_list__[N]);
  for(int i=0; i<N; ++i){
    std::cout<<random_list__[i]<<std::endl;
  }
}

fizz_rnd_list::~fizz_rnd_list(){
  delete [] random_list__;
}

double fizz_rnd_list::get_mean(int X_ind){
  double cur_tot = 0;
  for(int i=0; i<(X_ind+1); ++i){
    cur_tot+=random_list__[i]; 
  }
  return cur_tot/(float)(X_ind+1);
}

double fizz_rnd_list::get_std_dev(int X_ind){
  double cur_tot = 0;
  for(int i=0; i<(X_ind+1); ++i){
    cur_tot+=(random_list__[i]-x_mean)*(random_list__[i]-x_mean); 
  }
  return sqrt(cur_tot/(float)(X_ind+1));
}

std::tuple<double, int, double, double> fizz_rnd_list::get_stats(double X){
  if(cur_N==0){
    std::cerr<<"ERROR: Random array has no entries"<<std::endl;
    exit(EXIT_FAILURE);
  } 
  int cur_index = -1;
  double close_val = -1;
  int cur_len = cur_N; 
  double* cur_list = random_list__;
  while(cur_len>1){
    double *firstHalf = &cur_list[0];
    double *secondHalf = &cur_list[cur_len/2];
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
      cur_len = (cur_len/2);
      cur_list = secondHalf;
    }
    if(cur_len==1){
      close_val=cur_list[0];
    }
  }
  x_mean = get_mean(cur_index);
  double std_dev = get_std_dev(cur_index);
  return std::make_tuple(close_val,cur_index,x_mean,std_dev);
}

int main(int argc, char* argv[]){
  if(argc != 3) return -1;
  float num = atof(argv[1]);
  std::string in_string(argv[2]);
  fizz_rnd_list f_rnd(num);
  int_rnd_list i_rnd(num);
  std::tuple<double,int,double,double> fin_tup;
  double rand_num;
  if(in_string=="thousand"){
    rand_num = rand() % 1000;
    fin_tup = i_rnd.get_stats(rand_num);
  }
  if(in_string=="one"){
    rand_num = (float)rand()/(float)(RAND_MAX);
    fin_tup = f_rnd.get_stats(rand_num); 
  }
  //The following will print the tuple if you want. Could make this a function
  std::cout<<rand_num<<" "<<std::get<0>(fin_tup)<<" "<<std::get<1>(fin_tup)<<" "<<std::get<2>(fin_tup)<<" "<<std::get<3>(fin_tup)<<std::endl;

}

