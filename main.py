import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Source # is needed to install graphviz in the docker container
import os
   
from collections import OrderedDict

def plot_graph(G):
   A = nx.nx_agraph.to_agraph(G)

   os.remove('./dot/graph.dot') if os.path.exists('./dot/graph.dot') else None
   os.remove('./image/graph.gv') if os.path.exists('./image/graph.gv') else None

   A.write('./dot/graph.dot')
   s = Source.from_file('./dot/graph.dot')
   s.render('./image/graph.gv', format='jpg', view=True)

def get_n_highest_values(data, n=2, order=False):
    top = sorted(data.items(), key=lambda x: x[1], reverse=True)[:n]
    if order:
        return OrderedDict(top)
    return dict(top)

def main():
   if not os.path.isdir('./dot'):
      os.makedirs('./dot')

   if not os.path.isdir('./image'):
      os.makedirs('./image')

   # Load data
   df = pd.read_csv('data.csv', comment='#', sep=', ', header=0, engine='python')

   G = nx.DiGraph()
   G.add_weighted_edges_from(
      df[['id_sender', 'id_reciever', 'value']]
         .astype({'id_sender': str, 'id_reciever': str, 'value': float})
         .values
   )

   # isso aqui eh os nodes que tem a maior quantidade de shortest paths
   centrality = nx.betweenness_centrality(G)

   # Measures the number of edges connected to a node. Nodes with higher degree centrality are well-connected
   # olhar os valores mais altos, pois se algum desses falhar, problemas podem acontencer
   degree_cent = nx.degree_centrality(G)

   # Measures how close a node is to all other nodes, based on the shortest paths. Higher closeness centrality means the node can reach others more quickly
   close_cent = nx.closeness_centrality(G)

   # Find affected topics if a node is removed
   # impact = len(nx.descendants(G, 'data_structures'))

   print(centrality)
   print(get_n_highest_values(centrality))
   print(degree_cent)
   print(close_cent)
   # all the weights from the edges
   print(G.size(weight='weight'))
   # print(impact)

   # plot_graph(G)

main()
