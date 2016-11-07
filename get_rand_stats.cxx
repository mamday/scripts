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
  std::cout<<"Double "<<cur_N<<std::endl;
}

std::tuple<int, int, double, double> fizz_rnd_list::get_stats(int X){
  std::cout<<"Int "<<cur_N<<std::endl;

}

int main(){
  float num = 10.0;
  int i_num = 10;
  fizz_rnd_list f_rnd(num);
  int_rnd_list i_rnd(num);
  i_rnd.get_stats(i_num);
}

