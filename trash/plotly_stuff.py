import numpy as np
import plotly.express as px
import csv

######################################################################################################################################################################################

# Function f(x)
def f(x):
    return x**2

# Derivative of f with respect to x
def df_dx(x):
    return 2*x

# Newtons method to approximate a solution to a function
def newtons_method(f, df_dx, x0, tol=1e-6, max_iter=100):
    iter = 0 # Iteration counter starts at 0
    
    # Iterate and find an approximation
    while iter < max_iter:
        
        # If f(x) is smaller than the tolerance, then a good enough approximation has been found
        if abs(f(x0)) < tol:
            return x0
        
        x0 = x0 - f(x0) / df_dx(x0)
        iter += 1
        
    return x0

# Function to get the data of a function in (x, f(x)) format
def get_function_data(f, min_x, max_x, dx):
    return [[x, f(x)] for x in np.arange(min_x, max_x+1, dx)]

######################################################################################################################################################################################
x_val = np.arange(0, 10, 0.1)
y_val = f(x_val)
fig = px.line(x_val, y_val)
fig.show()

    

    