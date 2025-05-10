from plotnine import *
from plotnine.data import mtcars

# Create a scatter plot with regression lines, colored by cylinder
p = (ggplot(mtcars, aes(x='wt', y='mpg', color='factor(cyl)')) +
     geom_point() +  # Add scatter points
     geom_smooth(method='lm') +  # Add linear regression lines for each group
     labs(title='MPG vs Weight by Cylinder', x='Weight', y='MPG', color='Cylinders') +
     theme_minimal())  # Use a minimal theme for a clean look

# Display the plot (works in interactive environments like Jupyter)
print(p)

# Optional: Save the plot to a file (uncomment for non-interactive environments)
p.save('mpg_vs_weight.png')