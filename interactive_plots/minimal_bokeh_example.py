from bokeh.plotting import figure, show
import numpy as np
# Minimal example of using Bokeh to plot data in a web browser
# Krystof Hes
# 25.12.2023

x=np.linspace(0,10, 11)
y=2*x
# Create a figure
p = figure(title="Minimal example of line plot", x_axis_label="x", y_axis_label="y label")
# Plot a line
p.line(x,y, legend_label="example line", color='blue')
show(p)