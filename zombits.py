#test = [[1,2],[4,5],[7,9],[2,4]]
#g_test = [[10,14],[4,18],[19,20],[19,20],[13,20]]
#n_test = [[1,3],[3,6]]
h_test = [[1,2],[99,100],[100,102]]

import numpy
cur_test = h_test 
#Sort the list
cur_test.sort()

def answer(intervals):

    # your code here

    min_val=2^30

    max_val=-1

    cur_hours=0

    intervals.sort()

    for time in intervals:

        high_val = time.pop()

        low_val = time.pop()

        if(low_val<min_val):

            min_val=low_val

        if(high_val>max_val):

            if(low_val<=max_val):

                min_val=max_val
                max_val = high_val
                cur_hours+=max_val-min_val

            else:

                cur_hours+=high_val-low_val

                max_val=high_val

    return cur_hours

