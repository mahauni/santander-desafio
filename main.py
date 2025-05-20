import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

import warnings

# Load data
df = pd.read_csv('data.csv', comment='#', sep=', ', header=0, engine='python')

G = nx.DiGraph()
G.add_weighted_edges_from(
    df[['id', 'id_reciever', 'value']]
        .astype({'id': str, 'id_reciever': str, 'value': float})
        .values
)

elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 500]
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 500]

pos = nx.spring_layout(G, seed=10)  # positions for all nodes - seed for reproducibility

# nodes
nx.draw_networkx_nodes(G, pos, node_size=700)

# edges
nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
nx.draw_networkx_edges(
    G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed"
)

# node labels
nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
# edge weight labels
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels)

ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()
plt.show()

