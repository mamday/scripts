#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
#include "get_rand_stats.h"

int_rnd_list::int_rnd_list(int N):fizz_rnd_list(N){

}

int_rnd_list::~int_rnd_list(){

}

fizz_rnd_list::fizz_rnd_list(float N): cur_N(static_cast<int>(N)){
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

fizz_rnd_list::fizz_rnd_list(int N): cur_N(N){
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
    std::cout<<"Debug "<<cur_list[0]<<" "<<cur_list[cur_len/2]<<" "<<cur_len<<" "<<cur_index<<std::endl;
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
  std::cout<<"End "<<close_val<<" "<<cur_index<<std::endl;
}

int main(){
  float num = 10.0;
  int i_num = 10;
  fizz_rnd_list f_rnd(num);
  int_rnd_list i_rnd(num);
  f_rnd.get_stats(0.4); 
  i_rnd.get_stats(500);
}

