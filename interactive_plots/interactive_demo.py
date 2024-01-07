from bokeh.plotting import figure, show
from bokeh.layouts import row,column  # sorting the widgets on page
from bokeh.models import CustomJS, ColumnDataSource, Slider # models for callbacks, widgets
import numpy as np
# Bokeh - interactive plot
# Krystof Hes
# 25.12.2023

x=np.linspace(0,10, 200)
y=np.sin(x)

source = ColumnDataSource(data={'x':x, 'y':y})

# Create a figure
p = figure(title="Sine function", x_axis_label="x", y_axis_label="sin(x)")
# Plot a line
# p.line(x,y, legend_label="sin(x)", color='blue')
p.line('x', 'y', source=source)
amp = Slider(start=0.1, end=10, value=1, step=.1, title="Amplitude")
callback = CustomJS(args=dict(source=source, amp=amp),
                    code="""
    const A = amp.value
    const x = source.data.x
    const y = Array.from(x, (x) => A*Math.sin(x))
    source.data = { x, y }
""")
amp.js_on_change('value', callback) # add the callback function to the element
show(row(p, column(amp))) # row layout