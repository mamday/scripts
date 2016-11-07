#include <string>
#include <iostream>
#include <tuple>
#include <array>

class fizz_rnd_list{
  public:
    fizz_rnd_list(int N);
    virtual ~fizz_rnd_list();
    std::tuple<double, int, double, double> get_stats(double X);
  private:
    double* random_list__;
};
