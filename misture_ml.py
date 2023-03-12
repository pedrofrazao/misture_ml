import sys
import data



if __name__ == "__main__":
    f = "data2.csv"
    if( len(sys.argv) > 1 ):
        f = sys.argv[1]
    r = data.read_from_csv_to_array( f )
    print(r)
    errstr = data.check_array_data( r )
    if( errstr is not None ):
        print( errstr )