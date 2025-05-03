import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

G = nx.Graph()
G.add_nodes_from(["A", "B", "C", "D", "E"])
G.add_edges_from([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")])

# Generate a random seed and print it
seed = random.randint(0, 1000000)  # Generates a random integer between 0 and 1,000,000
print(f"Using seed: {seed}")

# Create a random state with the seed
random_state = np.random.RandomState(seed)

# Compute node positions using the random state
pos = nx.spring_layout(G, seed=random_state)

nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
nx.draw_networkx_edges(G, pos, width=2, alpha=0.5, edge_color='gray')   
nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
plt.title("Network Graph")
plt.figtext(0.5, 0.01, f"Seed: {seed}", ha="center", fontsize=10, color="gray")  # Add a footer to the plot
plt.axis('off')  # Turn off the axis
plt.show()
