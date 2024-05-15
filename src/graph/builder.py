import networkx as nx

class GraphBuilder:
    """Class to build a graph from nodes and edges."""

    def create_graph(self, nodes_df, edges_df):
        """
        Creates a graph using networkx from nodes and edges DataFrame.

        Parameters:
        nodes_df (pd.DataFrame): DataFrame containing node data.
        edges_df (pd.DataFrame): DataFrame containing edge data.

        Returns:
        networkx.DiGraph: Directed graph constructed from nodes and edges.
        """
        G = nx.DiGraph()
        for _, row in nodes_df.iterrows():
            G.add_node(row['ecli'], **row.to_dict())
        for _, row in edges_df.iterrows():
            G.add_edge(row['source'], row['target'])
        return G

