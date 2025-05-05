import pandas as pd
import matplotlib.pyplot as plt

data = {
    'Category': ['A', 'B', 'C', 'D', 'E'],
    'Values': [10, 20, 15, 5, 50]}

df = pd.DataFrame(data)
df.sort_values(by='Values', ascending=False, inplace=True)
df['Cumulative'] = df['Values'].cumsum()

df['Cumulative_Percentage'] = df['Cumulative'] / df['Values'].sum() * 100

fig, axl = plt.subplots(figsize=(10, 6))
axl.bar(df['Category'], df['Values'], color='blue', alpha=0.6, label='Values')
axl.set_ylabel('Values')
axl.set_xlabel('Category')

ax2 = axl.twinx()
ax2.plot(df['Category'], df['Cumulative_Percentage'], color='red', marker='o', label='Cumulative Percentage')
ax2.set_ylabel('Cumulative Percentage')

ax2.set_ylim(0, 100)
axl.set_title('Pareto Chart')

axl.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.grid()
plt.show()