import pandas as pd
import networkx as nx
from graphviz import Source
import os

from collections import OrderedDict

CURR_DIR = os.path.dirname(os.path.abspath(__file__))


def plot_graph(G, show_image_os):
    A = nx.nx_agraph.to_agraph(G)

    if not os.path.isdir(CURR_DIR + "/../dot"):
        os.makedirs(CURR_DIR + "/../dot")

    if not os.path.isdir(CURR_DIR + "/../image"):
        os.makedirs(CURR_DIR + "/../image")

    (
        os.remove(CURR_DIR + "/../dot/graph.dot")
        if os.path.exists(CURR_DIR + "/../dot/graph.dot")
        else None
    )
    (
        os.remove(CURR_DIR + "/../image/graph.gv")
        if os.path.exists(CURR_DIR + "/../image/graph.gv")
        else None
    )

    A.write(CURR_DIR + "/../dot/graph.dot")
    s = Source.from_file(CURR_DIR + "/../dot/graph.dot")
    if show_image_os:
        s.render(CURR_DIR + "/../image/graph.gv", format="jpg", view=True)


def get_n_highest_values(data, n=2, order=False):
    top = sorted(data.items(), key=lambda x: x[1], reverse=True)[:n]

    if order:
        return OrderedDict(top)
    return dict(top)


def populate_data():
    df = pd.read_csv("data.csv", comment="#", sep=", ", header=0, engine="python")

    G = nx.DiGraph()
    G.add_weighted_edges_from(
        df[["id_sender", "id_reciever", "value"]]
        .astype({"id_sender": str, "id_reciever": str, "value": float})
        .values
    )

    return G


def make_analysis():
    G = populate_data()

    # isso aqui eh os nodes que tem a maior quantidade de shortest paths
    centrality = nx.betweenness_centrality(G)

    # Measures the number of edges connected to a node. Nodes
    # with higher degree centrality are well-connected
    # olhar os valores mais altos, pois se algum desses falhar,
    # problemas podem acontencer
    degree_cent = nx.degree_centrality(G)

    # Measures how close a node is to all other nodes, based on the shortest paths.
    # Higher closeness centrality means the node can reach others more quickly
    close_cent = nx.closeness_centrality(G)

    plot_graph(G, False)

    # Centralize all the results to send to the frontend
    result = [
        (
            get_n_highest_values(centrality),
            f"Esses sao os nodes mais vitais, pois eles retem bastante do trafico: {get_n_highest_values(centrality)}",
        ),
        (
            get_n_highest_values(degree_cent),
            f"Esse sao os nodes que as maiores conexoes entre nodes: {get_n_highest_values(degree_cent)}",
        ),
        (
            get_n_highest_values(close_cent),
            f"Esse sao os nodes que estao mais pertos de todos os outros nodes: {get_n_highest_values(close_cent)}",
        ),
        (
            G.size(weight="weight"),
            f"Esse caso do valor total do mapa: {G.size(weight='weight')}",
        ),
    ]

    return result


def impact_on_remove(id):
    G = populate_data()

    impact = nx.descendants(G, id)

    return (
        impact,
        f"Essa e a quantidade de nodes impactados quando removido: {impact}",
    )


def main():
    if not os.path.isdir("./dot"):
        os.makedirs("./dot")

    if not os.path.isdir("./image"):
        os.makedirs("./image")

    # result = make_analysis()

    # print(result)
