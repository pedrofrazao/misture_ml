import numpy as np
import sys
import csv

def read_from_csv_to_list( filename ):
    """parse the CSV file and add all the data to a array"""
    entries = []
    with open( filename, newline='') as csvfile:
        row = csv.reader(csvfile, delimiter=';')
        for field in row:
            row_values = []
            for c in field:
                if( c[0] == "[" and c[-1] == "]" ):
                    # categorical values
                    cat = c[1:-1].split(',')
                    row_values.append( [ int( i ) for i in cat ] )
                else:
                    row_values.append( int(c) if c.isnumeric() else c )
            entries.append( row_values )
    return entries
            
def read_from_csv_to_array( filename ):
    """parse the CSV file and add all the data to a array"""
    entries = []
    with open( filename, newline='') as csvfile:
        row = csv.reader(csvfile, delimiter=';')
        for field in row:
            row_values = []
            r = None
            for c in field:
                if( c[0] == "[" and c[-1] == "]" ):
                    # categorical values
                    cat = c[1:-1].split(',')
                    r = np.array( [ int( i ) for i in cat ] )
                else:
                    r = int(c) if c.isnumeric() else c
                row_values.append( r )
            ar = np.array( row_values )
            entries.append( ar )
    return np.array( entries )


if __name__ == "__main__":
    f = "data1.csv"
    if( len(sys.argv) > 1 ):
        f = sys.argv[1]
    r = read_from_csv_to_array( f )
    print(r)