import pandas as pd
import networkx as nx
from graphviz import Source
import os

from collections import OrderedDict, deque

from typing import List

CURR_DIR = os.path.dirname(os.path.abspath(__file__))


def set_diff(sets: List[set]) -> set:
    sd = set()
    goners = set()
    for s in sets:
        sd ^= s - goners
        goners |= s - sd
    return sd


def plot_graph(G, show_image_os, imp_points):
    if not os.path.isdir(CURR_DIR + "/../../../dot"):
        os.makedirs(CURR_DIR + "/../../../dot")

    if not os.path.isdir(CURR_DIR + "/../../../image"):
        os.makedirs(CURR_DIR + "/../../../image")

    (
        os.remove(CURR_DIR + "/../../../dot/graph.dot")
        if os.path.exists(CURR_DIR + "/../../../dot/graph.dot")
        else None
    )
    (
        os.remove(CURR_DIR + "/../../../image/graph.gv")
        if os.path.exists(CURR_DIR + "/../../../image/graph.gv")
        else None
    )

    A = nx.nx_agraph.to_agraph(G)

    A.node_attr["fixedsize"] = True
    A.node_attr["height"] = 1.5
    A.node_attr["width"] = 2.0
    A.node_attr["style"] = "filled"
    # A.node_attr["concentrate"] = True # this will only work without labels
    # A.node_attr["layout"] = "twopi"

    for point in imp_points:
        if not hasattr(point[0], "__iter__"):
            continue

        for id in point[0]:
            n = A.get_node(id)
            n.attr["fillcolor"] = point[2]  # type: ignore[attr-defined]

    A.write(CURR_DIR + "/../../../dot/graph.dot")
    s = Source.from_file(CURR_DIR + "/../../../dot/graph.dot")

    s.render(CURR_DIR + "/../../../image/graph.gv", format="jpg", view=show_image_os)


def get_n_highest_values(data, n=2, order=False):
    top = sorted(data.items(), key=lambda x: x[1], reverse=True)[:n]

    if order:
        return OrderedDict(top)
    return dict(top)


def populate_data(full: bool, node: str, len: int):
    # make later so that it transforms to json, so the transition will be easier
    # if its uses gRPC now its a different problem that i'm wiling to use if I know
    # they use it
    df = pd.read_csv("data.csv", comment="#", sep=", ", header=0, engine="python")

    df = treat_data(df)

    G = nx.DiGraph()
    G.add_weighted_edges_from(
        df[["id_sender", "id_reciever", "value"]]
        .astype({"id_sender": str, "id_reciever": str, "value": float})
        .values
    )

    if full:
        G = treat_graph(G, node, len)

    return G


def get_n_level_descendants_bfs(G, node, n_levels=2):
    """
    Usa BFS para pegar descendentes até N níveis
    Mais eficiente para grafos grandes
    """
    if node not in G:
        return set()

    visited = {node}
    queue = deque([(node, 0)])  # (nó, nível)

    while queue:
        current_node, level = queue.popleft()

        if level < n_levels:
            for successor in G.successors(current_node):
                if successor not in visited:
                    visited.add(successor)
                    queue.append((successor, level + 1))

    return visited


def treat_graph(G, main_node, n_levels=2):
    nodes_to_keep = get_n_level_descendants_bfs(G, main_node, n_levels)
    nodes_to_remove = set(G.nodes()) - nodes_to_keep
    G.remove_nodes_from(nodes_to_remove)
    return G


def treat_data(data) -> pd.DataFrame:
    data["value"] = data["value"].str.lstrip("R$ ")
    data["value"] = data["value"].str.replace(",", "").astype(float)

    data = data.groupby(["id_sender", "id_reciever"], as_index=False)["value"].sum()

    return data


def make_analysis(full=False, node="CNPJ_01982", len=2):
    G = populate_data(full, node, len)

    # isso aqui eh os nodes que tem a maior quantidade de shortest paths
    centrality = nx.betweenness_centrality(G)
    centrality = get_n_highest_values(centrality)

    # Measures the number of edges connected to a node. Nodes
    # with higher degree centrality are well-connected
    # olhar os valores mais altos, pois se algum desses falhar,
    # problemas podem acontencer
    degree_cent = nx.degree_centrality(G)
    degree_cent = get_n_highest_values(degree_cent)

    # Measures how close a node is to all other nodes, based on the shortest paths.
    # Higher closeness centrality means the node can reach others more quickly
    close_cent = nx.closeness_centrality(G)
    close_cent = get_n_highest_values(close_cent)

    result = [
        (
            centrality,
            "Esses sao os CNPJ que tem a maior quantidade de conexoes no sistema:",
            "#CCCCFF",
        ),
        (
            degree_cent,
            "Esse sao os CNPJ que mais tem conexoes no sistema:",
            "#e6ccff",
        ),
        (
            close_cent,
            "Esse sao os CNPJ que estao mais pertos de outros CNPJ no sistema:",
            "#cce6ff",
        ),
        (
            G.size(weight="weight"),
            f"Esse caso do valor total do mapa: R$ {G.size(weight='weight')}",
        ),
    ]

    plot_graph(G, False, result)

    return result


def impact_on_remove(id: int, full=False, node="CNPJ_01982", len=2):
    G = populate_data(full, node, len)

    impact = nx.descendants(G, id)

    return (
        impact,
        f"Essa e a quantidade de nodes impactados quando removido: {impact}",
    )
