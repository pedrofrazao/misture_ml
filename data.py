import numpy as np
import sys
import csv
import re

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
    header_v1 = True
    classes=[]
    labels=[]
    re_empty_line = re.compile("^\s*$")
    re_comment = re.compile("^#.*")
    re_empty_comment = re.compile("^#?\s+$")
    re_header = re.compile(r"^#\s*__header__")
    re_class = re.compile( r"^#\s*class\w+\s*:\s*([\d,-]+)" )
    re_label = re.compile( r"^#\s*label\w*\s*:\s*([\d,-]+)" )

    with open( filename, "r") as csvfile:
        for line in csvfile:
            ## ignore empty lines
            if( re_empty_line.match( line ) ):
                continue
            ## ignore comments
            if( re_empty_comment.match( line ) ):
                continue

            ## stop reading if is a line with data
            if( not re_comment.match( line ) ):
                break

            ## read header lines
            if( re_header.match( line ) ):
                header_v1 = False
            else:
                ## label
                m = re_label.match( line )
                if( m ):
                    labels.append( m.group(1) )
                    continue
                m = re_class.match( line )
                if( m ):
                    classes.append( m.group(1) )
    
    if( header_v1 ):
        return read_from_csv_to_array_v1( filename )
    return read_from_csv_to_array_v2( filename, labels, classes )

def read_from_csv_to_array_v2( filename, labels, classes ):
    """parse the CSV file and add all the data to a array"""
    entries = []

    with open( filename, newline='') as csvfile:
        row = csv.reader(csvfile, delimiter=',')
        re_comment = re.compile("^#")

        for field in row:
            if( len(field) == 0
                or re_comment.match(field[0] ) ):
                continue
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
            _append_on_entries( entries, row_values, labels, classes )
#            ar = np.array( row_values, dtype=object )
#            entries.append( ar )
    return np.array( entries, dtype=object)


def _append_on_entries( entries, values, labels, classes ):
    row = []
    ## add label if any
    if( len( labels ) > 0 ):
        row.append( values[ int(labels[0] ) -1 ] )
    
    ## add classes
    re_range = re.compile(r'^(\d+)-(\d+)$')
    for c in classes:
        ## range class
        m = re_range.match( c )
        if( m ):
            istart = int( m.group(1) ) -1
            istop = int( m.group(2) )
            row.append( np.array( values[ istart:istop ] ) )
        else:
            print(f'ERROR: fail to process class definition {c}')
            sys.exit(3)

    entries.append( row )
    return

def read_from_csv_to_array_v1( filename ):
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
            ar = np.array( row_values, dtype=object )
            entries.append( ar )
    return np.array( entries, dtype=object)


def check_array_type_on_array_class( arraycolumn ):
    """check if all values are of the same type on the array"""
    error = None
    class_sum = arraycolumn[0].sum()
    for i in range(1,len(arraycolumn)):
        sum=arraycolumn[i].sum()
        if(class_sum != sum):
            error=f'found a different sum for class in position {i+1}: got {sum} and expecting {class_sum}'
            break
    return error


def check_array_type_values( arraycolumn ):
    """check if all values are of the same type on the array"""
    error = None
    vtype = type( arraycolumn[0] )
    if( vtype == np.ndarray ):
        return check_array_type_on_array_class( arraycolumn )
    for i in range(1,len(arraycolumn)):
        if( type(arraycolumn[i]) != vtype ):
            error=f'found a different type on array in position {i+1}'
            break
    return error


def check_array_data( arraydata ):
    """check that the array have the proper format"""
    errstr = None
    r,c=arraydata.shape

    for i in range(0,c):
        err = check_array_type_values( arraydata[:,i] )
        if(err is not None):
            errstr = f'ERROR: on column {i} - {err}'
            return errstr

    sum_val = sum_by_class( arraydata[0] )
    min_val = sum_val[ ~np.isnan(sum_val) ].min()
    max_val = sum_val[ ~np.isnan(sum_val) ].max()

    if( min_val != max_val ):
        errstr = f"ERROR: some classes sum to != values: {sum_val}"
        return errstr

def sum_by_class( data ):
    """return the sum by classes"""
    c = data.shape[0]
    sum_by_class = np.zeros(c)
    for i in range(0,c):
        sum_by_class[i] = data[i].sum() if( type(data[i]) == np.ndarray ) else None
        if( sum_by_class[i] is not None ):
            continue
        else:
            if( sum_val is None ):
                sum_val = sum_by_class[i]
    return sum_by_class

def get_sum_classes( data ):
    """return the sum of classes"""
    d = sum_by_class( data[0] )
    d = d[ ~np.isnan(d) ]
    return d[0]

def get_num_cat( data ):
    """return list of category dimention"""
    return [ len(v) if( type(v) == np.ndarray ) else 0 for v in data[0] ]

def get_num_variable( data ):
    """return number of variables"""
    d=[  1 if( type(v) == np.ndarray) else 0 for v in data[0] ]
    return sum(d)

if __name__ == "__main__":
    f = "data4.csv"
    if( len(sys.argv) > 1 ):
        f = sys.argv[1]
    r = read_from_csv_to_array( f )
    print(r)
    errstr = check_array_data( r )
    if( errstr is not None ):
        print( errstr )
    
    print( sum_by_class(r[0]) )

    print( "dim_multinomial: " + str( get_sum_classes(r)) )
    print( "nvar: " + str( get_num_variable(r) ) )
    print( "num cat: " + str(get_num_cat(r)))