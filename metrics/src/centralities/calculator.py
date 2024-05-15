import networkx as nx

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

    def calculate_betweenness_centrality(self, G):
        """
        Calculates the betweenness centrality for each node in the graph.

        Parameters:
        G (networkx.DiGraph): The graph to analyze.

        Returns:
        dict: Dictionary of nodes with betweenness centrality as values.
        """
        return nx.betweenness_centrality(G)

    # Add more centrality measures as needed
