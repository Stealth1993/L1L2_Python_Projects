import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

years = ['2017', '2018', '2019', '2020', '2021', '2022']

languages = ['Python', 'Java', 'C++', 'JavaScript', 'Ruby', 'PHP']

rankings = [
    [8, 6, 5, 3, 2, 1], [1, 2, 2, 2, 3, 2],
    [10, 9, 8, 5, 5, 3], [2, 3, 3, 4, 4, 4],
    [5, 4, 4, 6, 6, 5],
]

colors = ['lime', 'magenta', 'cyan', 'orange', 'purple', 'red']

plt.figure(figsize=(12, 6))

for i, (language, ranking) in enumerate(zip(languages, rankings)):
    plt.plot(years, ranking, marker='o', color=colors[i], label=language)
    plt.fill_between(years, ranking, color=colors[i], alpha=0.1)

plt.gca().invert_yaxis()
plt.xticks(years, fontsize=10)
plt.yticks(np.arange(1, 13), fontsize=10)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Ranking', fontsize=12)
plt.title('Programming Language Popularity Over Time', fontsize=14)
plt.legend(title='Languages', fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

plt.show()