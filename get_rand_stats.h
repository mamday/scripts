#include <string>
#include <iostream>
#include <tuple>
#include <array>
#include <unordered_map>

//This class creates a list of random values either between 0-1 (if it is 
//initialized with a float) or between 0-1000 (if it is initialized with an
// integer). The method get_stats(X) will then find the value in the random 
//list that is closest to X and the index of that value. It then outputs the
// mean  and standard deviation of all entries of the list up to that value.
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
    double get_uniform_std_dev(int X_ind);
    //A getter for the random_list__ 
    double* get_list();
  private:
    //Array to hold the list of random numbers
    double* random_list__;
    //Length of the array of random numbers
    int cur_N__;
    //Mean from get_mean()
    double x_mean__;
    //A map of all values of the mean. Use unordered_map because lookup is O(1)
    std::unordered_map<int,double> mean_map__;
    //A map of all values of the standard deviation. 
    //Use unordered_map because lookup is O(1)
    std::unordered_map<int,double> std_dev_map__;
    //The current highest value in the mean map
    int max_mean_ind__;
};

//This class inherits from fizz_rnd_list, but always calls its integer 
//constructor (so that the random list has values from 0-1000)
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

class test_rnd_list{
  public:
    test_rnd_list();
    virtual ~test_rnd_list();

    void test_fizz_rnd_list_initiation();
    void test_int_rnd_list_initiation();
    void test_uniform_std_dev();
    void test_get_mean_zero();
    void test_get_std_dev_zero();
    void test_get_mean_one();
    void test_get_std_dev_one();
    void test_get_mean_two();
    void test_get_mean_repeat();
    void test_get_mean_threepeat();
    void test_get_stats();
};
