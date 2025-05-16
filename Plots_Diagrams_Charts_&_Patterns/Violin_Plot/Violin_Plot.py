import seaborn as sns
import matplotlib.pyplot as plt


#dummy data
import pandas as pd
import numpy as np

np.random.seed(0)
data = pd.DataFrame({
    "Category": np.random.choice(["A", "B", "C"], size=100),
    "Value": np.random.randn(100)
})

# Create a violin plot
plt.figure(figsize=(10, 6))
sns.violinplot(x="Category", y="Value", data=data, inner="quartile")
plt.title("Violin Plot Example")
plt.xlabel("Category")
plt.ylabel("Value")
plt.grid(True)
plt.show()