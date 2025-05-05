import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

df = sns.load_dataset("iris")
sns.pairplot(df, hue="species", palette="Set2")
plt.suptitle("Pair Plot of Iris Dataset", y=1.02)
plt.show()
