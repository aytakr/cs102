from api import get_friends
from igraph import plot, Graph
import numpy as np
import igraph

def get_network(*users_ids, as_edgelist=True):

    vertices = [i for i in range(len(users_ids))]
    edges = []

    for i in range(len(users_ids)):
        for j in range(len(users_ids)):
            try:
                if users_ids[i] in get_friends(users_ids[j], '').json()['response']['items']:
                    edges.append((i, j))
            except:
                pass

    g = Graph(vertex_attrs={"label":vertices}, edges=edges, directed=False)

    plot_graph(g, vertices)


def plot_graph(g, vertices):

    N = len(vertices)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=1000,
        area=N**3,
        repulserad=N**3)

    g.simplify(multiple=True, loops=True)

    communities = g.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()

    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)

    plot(g, **visual_style)
