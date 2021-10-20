from atc import *

#Call the main_solver(f,n,value_list) function to get the output.

# Input Parameters

# f --- > Z3 General Formula (Quantifier-Free) :: Check ReadMe for more info.
# n --- > Total Number of variables used.
# value_list --- > python-list which contains the values for x_i's in sequencial order. So first element will be value for x1 and last will be value for xn.

# Output Format --- > The function returns nothing, but prints out all required information to STDOUT.

#For details regarding other functions , check ReadMe

# No need to import z3 here to define the z3 formulas, it is already there in atc.py

# Type your code here .....

x1 = Int('x1')
x2 = Int('x2')
x3 = Int('x3')

function = And(x1+x2+x3<=10, Not(x1==3))


n = 3


value_list = [4,4,1]


main_solver(function,n,value_list)