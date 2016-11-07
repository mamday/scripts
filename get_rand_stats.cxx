#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include "get_rand_stats.h"

fizz_rnd_list::fizz_rnd_list(int N){
  random_list__ = new double[N]();
  srand((unsigned int) time(NULL));
  for(int i=0; i<N; ++i){
    random_list__[i]=((float)rand()/(float)(RAND_MAX));
  }
  for(int i=0; i<N; ++i){
    std::cout<<random_list__[i]<<std::endl;
  }
}

fizz_rnd_list::~fizz_rnd_list(){
  delete [] random_list__;
}

int main(){
  fizz_rnd_list rnd(10);
}

