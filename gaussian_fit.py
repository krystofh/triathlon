import os
import pandas as pd
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm
import numpy as np
import statistics

# Example of fitting a histogram with gaussian curve
# Date: 24.12.2023

# Create data
data = np.random.normal(60, 10, 200) # numpy has random function with normal distribution (or others)
# Calculating mean and standard deviation 
mean, std = norm.fit(data)
    
# Create and plot histogram
counts, bin_edges = np.histogram(data, bins=10, density=True)
plt.hist(data, density=True)
# Plot the PDF. 
xmin, xmax = plt.xlim() 
x = np.linspace(xmin, xmax, 100) 
p = norm.pdf(x, mean, std) 
plt.plot(x, p, 'k', linewidth=2) 

plt.show()
print("Done")