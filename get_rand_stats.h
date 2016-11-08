#include <string>
#include <iostream>
#include <tuple>
#include <array>

class fizz_rnd_list{
  public:
    //Constructors that take the number N of random numbers as its argument
    //Where N is either an integer or a float depending on what range of random
    //numbers you want (float: 0-1, integer: 0-1000) 
    fizz_rnd_list(int N);
    fizz_rnd_list(float N);
    //Destructor
    virtual ~fizz_rnd_list();
    //Function to calculate the value and index of the closest item to X.
    //Then find the mean and standard deviation of the entries up to the index.
    std::tuple<double, int, double, double> get_stats(double X);
    double get_mean(int X_ind);
    double get_std_dev(int X_ind);
  private:
    //Array to hold the list of random numbers
    double* random_list__;
    //Length of the array of random numbers
    int cur_N;
    //Mean from get_mean()
    double x_mean;
};

class int_rnd_list: public fizz_rnd_list{
  public:
    //Constructor that takes the number N of random numbers as its argument 
    int_rnd_list(int N);
    //Destructor
    ~int_rnd_list();
    // I don't choose to reimplement any of the functionality from the original
    // class, because this class can use it just as easily. I would probably
    // not create this second class at all, if I was being most efficient,
    // to save on having to call the virtual destructor
};
