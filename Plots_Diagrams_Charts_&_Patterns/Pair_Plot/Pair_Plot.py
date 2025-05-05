import matplotlib.pyplot as plt
import seaborn as sns

df = sns.load_dataset("iris")
sns.pairplot(df, hue="species", palette="Set1", diag_kind="kde",
                 markers=["o", "s", "D"], plot_kws={"alpha": 0.7, "s": 50})
plt.suptitle("Pair Plot of Iris Dataset", y=1.02)
plt.show()
