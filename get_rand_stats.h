#include <string>
#include <iostream>
#include <tuple>
#include <array>

class fizz_rnd_list{
  public:
    fizz_rnd_list(int N);
    fizz_rnd_list(float N);
    virtual ~fizz_rnd_list();
    std::tuple<double, int, double, double> get_stats(double X);
  private:
    double* random_list__;
    int cur_N;
};

class int_rnd_list: public fizz_rnd_list{
  public:
    int_rnd_list(int N);
    ~int_rnd_list();

};
