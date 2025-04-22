import matplotlib.pyplot as plt

# Create data
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
data2 = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
data3 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# create a box and whisker plot with custom colors

box_color = '#FF5733'  # Custom color for the box
whisker_color = '#33FF57'  # Custom color for the whiskers
median_color = '#3357FF'  # Custom color for the median line
flier_color = '#FF33A1'  # Custom color for the flier points

plt.boxplot([data, data2, data3],
              boxprops=dict(color=box_color),
              whiskerprops=dict(color=whisker_color),
              capprops=dict(color=whisker_color),
              medianprops=dict(color=median_color),
              flierprops=dict(marker='o', color=flier_color, alpha=0.5),
              patch_artist=True)

# Add title and labels
plt.title('Box and Whisker Plot with Custom Colors')
plt.xlabel('Data Sets')
plt.ylabel('Values')

# Show the plot
plt.show()

