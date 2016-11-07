#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include "get_rand_stats.h"

int_rnd_list::int_rnd_list(int N):fizz_rnd_list(N){

}

int_rnd_list::~int_rnd_list(){

}

fizz_rnd_list::fizz_rnd_list(float N){
  int int_N = static_cast<int>(N);
  random_list__ = new double[int_N]();
  srand((unsigned int) time(NULL));
  for(int i=0; i<int_N; ++i){
    random_list__[i]=((float)rand()/(float)(RAND_MAX));
  }
  for(int i=0; i<int_N; ++i){
    std::cout<<random_list__[i]<<std::endl;
  }
}

fizz_rnd_list::fizz_rnd_list(int N){
  random_list__ = new double[N]();
  srand((unsigned int) time(NULL));
  for(int i=0; i<N; ++i){
    random_list__[i]=rand() % 1000;
  }
  for(int i=0; i<N; ++i){
    std::cout<<random_list__[i]<<std::endl;
  }
}

fizz_rnd_list::~fizz_rnd_list(){
  delete [] random_list__;
}

int main(){
  float num = 10.0;
  int i_num = 10;
  fizz_rnd_list f_rnd(num);
  int_rnd_list i_rnd(num);
}

