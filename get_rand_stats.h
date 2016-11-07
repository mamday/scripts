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
    std::tuple<int, int, double, double> get_stats(int X);
  private:
    double* random_list__;
};

class int_rnd_list: public fizz_rnd_list{
  public:
    int_rnd_list(int N);
    ~int_rnd_list();

};
