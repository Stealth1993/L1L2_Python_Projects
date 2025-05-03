import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

G = nx.Graph()
G.add_nodes_from(["A", "B", "C", "D", "E"])
G.add_edges_from([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")])

pos = nx.spring_layout(G, seed=92)  # positions for all nodes

nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
nx.draw_networkx_edges(G, pos, width=2, alpha=0.5, edge_color='gray')   
nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
plt.title("Network Graph")
plt.axis('off')  # Turn off the axis
plt.show()
