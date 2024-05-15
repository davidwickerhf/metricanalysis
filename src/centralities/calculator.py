import networkx as nx
import numpy as np
from networkx.algorithms.centrality import (
    degree_centrality,
    betweenness_centrality,
    closeness_centrality,
    eigenvector_centrality_numpy,
    harmonic_centrality,
    current_flow_betweenness_centrality,
    current_flow_closeness_centrality,
)
from networkx.algorithms.link_analysis.hits_alg import hits
from networkx.algorithms.link_analysis.pagerank_alg import pagerank

from scipy.sparse.linalg import eigs

class CentralityCalculator:
    """Class to calculate various centrality measures for a graph."""

    def calculate_degree_centrality(self, G):
        """
        Calculates the degree centrality for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with degree centrality as values.
        """
        return nx.degree_centrality(G)

    def calculate_in_degree_centrality(self, G):
        """
        Calculates the in-degree centrality for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with in-degree centrality as values.
        """
        return dict(G.in_degree())

    def calculate_core_number(self, G):
        """
        Calculates the core number for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with core number as values.
        """
        return nx.core_number(G)

    def calculate_relative_in_degree_centrality(self, G):
        """
        Calculates the relative in-degree centrality for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with relative in-degree centrality as values.
        """
        in_degrees = dict(G.in_degree())
        num_nodes = len(G.nodes)
        return {node: degree / num_nodes for node, degree in in_degrees.items()}

    def calculate_eigenvector_centrality(self, G):
        """
        Calculates the eigenvector centrality for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with eigenvector centrality as values.
        """
        return nx.eigenvector_centrality_numpy(G)

    def calculate_pagerank(self, G):
        """
        Calculates the PageRank for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with PageRank as values.
        """
        return nx.pagerank(G)

    def calculate_current_flow_betweenness_centrality(self, G):
        """
        Calculates the current flow betweenness centrality for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with current flow betweenness centrality as values.
        """
        return current_flow_betweenness_centrality(G)

    def calculate_forest_closeness_centrality(self, G):
        """
        Calculates the forest closeness centrality for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with forest closeness centrality as values.
        """
        # Placeholder for actual implementation
        # This is a complex measure not natively supported by NetworkX
        return {}

    def calculate_hits(self, G):
        """
        Calculates the HITS algorithm (hubs and authorities) for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        tuple: Two dictionaries of nodes with hubs and authorities scores as values.
        """
        hubs, authorities = hits(G)
        return hubs, authorities

    def calculate_trophic_level(self, G):
        """
        Calculates the trophic level for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with trophic level as values.
        """
        # Placeholder for actual implementation
        # This is a specific measure from ecology
        return {}

    def calculate_betweenness_centrality(self, G):
        """
        Calculates the betweenness centrality for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with betweenness centrality as values.
        """
        return nx.betweenness_centrality(G)

    def calculate_current_flow_closeness_centrality(self, G):
        """
        Calculates the current flow closeness centrality for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with current flow closeness centrality as values.
        """
        return current_flow_closeness_centrality(G)

    def calculate_out_degree_centrality(self, G):
        """
        Calculates the out-degree centrality for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with out-degree centrality as values.
        """
        return dict(G.out_degree())

    def calculate_hub_centrality(self, G):
        """
        Calculates the hub centrality for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with hub centrality as values.
        """
        hubs, _ = hits(G)
        return hubs

    def calculate_authority_centrality(self, G):
        """
        Calculates the authority centrality for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with authority centrality as values.
        """
        _, authorities = hits(G)
        return authorities

    def calculate_harmonic_centrality(self, G):
        """
        Calculates the harmonic centrality for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with harmonic centrality as values.
        """
        return nx.harmonic_centrality(G)
    
    def get_neighbours(graph, node):
        incoming, outgoing = [], []
        graph.forInEdgesOf(node, lambda u, v, w, id: incoming.append(v))
        graph.forEdgesOf(node, lambda u, v, w, id: outgoing.append(v))
        return incoming, outgoing

    def calculate_disruption(self, G):
        """
        Calculates the disruption centrality for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with disruption centrality as values.
        """
        disruptions = np.zeros(G.numberOfNodes())
        for node in G.iterNodes():
            incoming, outgoing = self.get_neighbours(G, node)
            i, j, k = [], [], []
            for in_node in incoming:
                for out_node in outgoing:
                    # This method does not account for directedness, but this does not matter because ingoing and outgoing lists are used.
                    if G.hasEdge(in_node, out_node):
                        if not out_node in j:
                            j.append(out_node)
            for out_node in outgoing:
                if not out_node in j:
                    i.append(out_node)
            for in_node in incoming:
                _, outgoing = self.get_neighbours(G, in_node)
                for out_node in outgoing:
                    if not out_node in j and not out_node == node:
                        k.append(out_node)
            n_i, n_j, n_k = len(i), len(j), len(k)
            numerator, denominator = n_i-n_j, n_i+n_j+n_k
            disruption = numerator/denominator if denominator != 0 else np.nan
            disruptions[node] = disruption
        return disruptions

    def calculate_closeness_centrality(self, G):
        """
        Calculates the closeness centrality for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with closeness centrality as values.
        """
        return nx.closeness_centrality(G)