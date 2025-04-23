import matplotlib.pyplot as plt

categories = ['Category']
values =[75]
ranges = [(50, 100)]  # Range for the bullet chart
markers = [80]  # Marker for the bullet chart
fig, ax = plt.subplots(figsize=(8, 4))

ax.barh(categories, values, color='lightblue', edgecolor='black')

for i, (low, high) in enumerate(ranges):
    ax.plot([low, high], [i, i], color='red', linewidth=8, label='Range')
    ax.text(low, i, f'{low}', va='center', ha='right', color='black')
    ax.plot([markers[i]], [i], 'ro', markersize=10, label='Marker')

plt.title('Bullet Chart Example')
plt.show()