from bokeh.plotting import figure, show
from bokeh.models import HoverTool, ColumnDataSource
import numpy as np

# Generate sample data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Create ColumnDataSources for each line
source1 = ColumnDataSource(data=dict(x=x, y=y1))
source2 = ColumnDataSource(data=dict(x=x, y=y2))

# Create a figure with title and axis labels
p = figure(title="Sine and Cosine Waves", x_axis_label='X', y_axis_label='Y')

# Add line renderers for sine and cosine
p.line('x', 'y', source=source1, legend_label="sin(x)", line_width=2, color="blue")
p.line('x', 'y', source=source2, legend_label="cos(x)", line_width=2, color="red")

# Add hover tools for each line
hover1 = HoverTool(renderers=[p.renderers[0]], tooltips=[("Function", "sin(x)"), ("X", "@x"), ("Y", "@y")])
hover2 = HoverTool(renderers=[p.renderers[1]], tooltips=[("Function", "cos(x)"), ("X", "@x"), ("Y", "@y")])
p.add_tools(hover1, hover2)

# Display the plot (opens in a web browser)
show(p)