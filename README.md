# misture_ml #


`data` format something like. The first value is only an observation identifier.
```
[['a' array([1, 2, 3, 4, 5]) array([1, 2, 3]) array([1, 2, 3])]
 ['b' array([2, 1, 3, 4, 5]) array([2, 1, 3]) array([1, 2, 3])]
 ['c' array([3, 2, 1, 4, 5]) array([3, 2, 1]) array([1, 2, 3])]
 ['d' array([4, 3, 2, 1, 5]) array([1, 2, 3]) array([1, 2, 3])]]
```

`est_prob` - with the same structure of the data, but in each row represent a 1 segment, and in the column we have the probability of the class.

# TODO #

## data validation ##

the sum of each class need to be the same.
Ex, for the `a;[1,2,3,4,5];[1,2,3];[1,2,3]`, the 1st class sums 15 but the 2nd sums 6. It's wrong.


return the `dim_multinomial` value, that is the sum of any class.
return the number of variables - `nvar`. It's the number of columns.
return a list with the number of categories of each variable - `ncal_var`.

## init est_prob ##

Note: the `rand` return a value between ]0,1[.

To init `est_prob`

est_prob[0][1][category1] = (sum data[:][1][category1])/len(data)/dim_multinomial + small_value * dim_observations * rand() 

normalize for each category.

## init est_pp ##

initial estimates of the mixing probabilities

```
estpp[i] = ( 1 / k )
```

where:
- k - number os segments

## init semi_indic ##

```
semi_indic[i][k] = ( N! )^nvar * ??????????????????
```

where:
- i - each observation
- k - num segments
- N - multinomial size
- `nvar`
