import matplotlib.pyplot as plt
import numpy as np

def spider_chart(data, categories, title='Spider Chart', save_path=None):
    # Number of variables
    num_vars = len(categories)

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # The plot is a circle, so we need to "complete the loop" and append the start to the end.
    data = np.concatenate((data, [data[0]]))
    angles += angles[:1]

    # Create the spider chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, data, color='blue', alpha=0.25)
    ax.plot(angles, data, color='blue', linewidth=2)

    # Labels for each axis
    plt.xticks(angles[:-1], categories)

    # Title
    plt.title(title)

    # Save or show the plot
    if save_path:
        plt.savefig(save_path)
        print(f"Spider chart saved to {save_path}")
    else:
        plt.show()