import sys
import numpy as np

import data as mml_data

small_value=np.float128(0.1)

def pp_calc_for_class( catvar,  dim_multinomial ):
    """ sum all classe vectors and """
    npoint = catvar.shape[0]  # number of observations
    t = sum(catvar) / ( npoint * dim_multinomial )
    return t

def pp_calc( y, dim_multinomial ):
    #pp = np.ndarray( [ pp_calc_for_class( k, y ) for k in range(0,len(y)) ] )
    #return pp
    t = [ pp_calc_for_class( y[:,i], dim_multinomial ) for i in range(0,y.shape[1]) ]
    return t

def init_est_prob( y ):
    """ init est_prob structure """
    #est_prob[0][1][category1] = (sum data[:][1][category1])/len(data)/dim_multinomial + small_value * dim_observations * rand() 
    pass

def init(y):
    pass

if __name__ == "__main__":
    f = "data2.csv"
    if( len(sys.argv) > 1 ):
        f = sys.argv[1]
    y = mml_data.read_from_csv_to_array( f )
    print(y)
    ylabel = y[:,0]
    y = y[:,1:]
    # print(y)
    errstr = mml_data.check_array_data( y )
    if( errstr is not None ):
        print( errstr )

    dim_multinomial = mml_data.get_sum_classes( y )
    pp = pp_calc( y, dim_multinomial )
    print(pp)