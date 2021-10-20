

# 1. Overview
All the necessary functions are implemented in the `atc.py` file. So to get the output you have to make use of this by importing it and calling appropriate functions.

I've already included a `main.py` where the input is to given , it would be better to make use of that to test my code. More details on how to provide the input to test is given in the following section.



## 1.1 Testing

In the `main.py` file I've already done the necessary imports from `atc.py`. Note that `z3` is already imported in `atc.py`, so don't import it again. Also make sure , both `main.py` and `atc.py` are in the same directory.

The function that you'll be using to get the output is:
```python3
main_solver(function,n,value_list)
```
Here,

`function` is standard a z3 general formula.

`n` is the total number of variables used in `function`

`value_list` is a python-list that will contain the decimal values for each x_i's in sequencial order. 

## 1.2 Z3 Function Format

Any general formula that is quantifier-free should work, but one thing is to be kept in mind.

Make sure, `And()` , `Or()` z3-functions are only given 2 parameters i.e. they should be of arity-2.  Z3 supports more than 2 parameters for `And()` and `Or()` , but my program cannot parse that.

So please convert any such `And()` or `Or()` as follows:

```
    And(f1,f2,f3) ==> And(And(f1,f2),f3)
    Or(f1,f2,f3) ==> Or(Or(f1,f2),f3)
```


## 1.3 Example
```python
x1 = Int('x1')
x2 = Int('x2')
x3 = Int('x3')

function = And(x1+x2+x3<=10, Not(x1==3))
n = 3
value_list = [4,4,1]
main_solver(function,n,value_list)
```
In the above example we have given our function as `(x1+x2+x3<=10 ^ x1!=3)`.

Also we're having 3 variables hence `n = 3`

We want to check if the automaton accepts when `x1=4` , `x2=4` and `x3=1`. Hence `value_list = [4,4,1]` 

## 1.4 Output Format

The DFA Transition-table is printed to `STDOUT`. The alphabet for each DFA is the bit-vector `(b1 b2 ... bn)`.

So the first bit, `b1` corresponds to `x1` and in general the ith bit, `bi` corresponds to `xi`.

In the table, the **Final States** are marked with `<F>` and the **Initial State** is marked with `<I>`.






