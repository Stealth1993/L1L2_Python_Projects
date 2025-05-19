import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#sample data
data = {
    'A': np.random.normal(0, 1, 1000),
    'B': np.random.normal(1, 2, 1000),
    'C': np.random.normal(2, 3, 1000)
}

df = pd.DataFrame(data)
# Create a histogram for each column in the DataFrame
for column in df.columns:
    plt.hist(df[column], bins=30, alpha=0.5, label=column)
plt.legend()
plt.show()