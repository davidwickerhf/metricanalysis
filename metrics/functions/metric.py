import abc, typing, os, datetime, dateutil.parser, statistics
from metrics.util.timer import timer
import matplotlib.pyplot as plt
import networkit as nk
import pandas as pd
import numpy as np

class Metric(abc.ABC):
    """
    Abstract metric class to be inherited by all metrics.

    Args:
        abc (_type_): _description_
    """
    def __init__(self, name: str, graph: nk.Graph, nodes_path: str, edges_path: str, graphs_path: str) -> None:
        super().__init__()
        self.name = name
        self.graph = graph
        self.eclis = []
        self.nodes_path = nodes_path
        self.edges_path = edges_path

    def __str__(self):
        return self.__class__.__name__
    
    # TODO Run the metric function
    @abc.abstractmethod
    @timer
    def run(self) -> None:
        pass
    
    # TODO Load the graph function
    @timer
    def load_graph(self, nodes: pd.DataFrame, edges: pd.DataFrame) -> nk.Graph:
        """
        Build a graph with ECLIs attached to each node.
        :param nodes: Nodes of the graph.
        :param edges: Edges of the graph.
        """
        graph = nk.Graph(directed=True)
        eclis = graph.attachNodeAttribute("eclis", str)
        for index, row in nodes.iterrows():
            node = graph.addNode()
            eclis[node] = row["ecli"]
            # os.system('cls' if os.name == 'nt' else 'clear')
            # print('Elapsed:  ', (int)(time.time() - start), '| begin_graph(): add node: ', index)

        for index, row in edges.iterrows():
            to_ecli = row["ecli"]
            if nodes["ecli"].eq(to_ecli).any():
                references = row["references"]
                for node in graph.iterNodes():
                    if eclis[node] == to_ecli:
                        v = node
                for from_ecli in references:
                    if nodes["ecli"].eq(from_ecli).any():
                        for node in graph.iterNodes():
                            if eclis[node] == from_ecli:
                                u = node
                        graph.addEdge(u, v) # is checkMultiEdge necessary?

            # if start:
            #     os.system('cls' if os.name == 'nt' else 'clear')
            #     print('Elapsed:  ', (int)(time.time() - start), '| begin_graph(): get ecli: ', to_ecli)
        graph.removeSelfLoops()
        self.graph = graph
        return self.graph


    # TODO Write the results function

    # TODO Graph the results function
    def _categorise_branch_numerically(self, branches: pd.Series) -> np.ndarray:
        """
        Convert branch categorisation from strings into numbers.
        :param branchs: The column containing branch data, categorised with strings.
        """
        numericised = np.zeros(len(branches))
        for instance_no in range(len(branches)):
            if branches[instance_no] == "GRANDCHAMBER":
                numericised[instance_no] = 1
            elif branches[instance_no] == "CHAMBER":
                numericised[instance_no] = 2
            elif branches[instance_no] == "COMMITTEE":
                numericised[instance_no] = 3
        return numericised

    def _prep_data(self, include: list, type: str) -> pd.DataFrame:
        """
        Prepare the dataset by selecting the appropriate headers, merging the key cases category with the high importance category if type merged is
            specified, or removing cases before 01/11.98, which is when key cases were introduced if unmerged is specified.
            Also filter out nodes with metric value of -2 (uncomputed values)
        :param include: Headers to include.
        :param type: How to deal with the late introduction of key cases.
        :return data: The processed data.
        """
        metadata = pd.read_csv(self.nodes_path).fillna(0)

        if type == "unmerged":
            cutoff_date = datetime.datetime(1998, 11, 1, 0, 0, 0).date()
            for index, row in metadata.iterrows():
                case_date = dateutil.parser.parse(row["judgementdate"], dayfirst=True).date()
                if case_date < cutoff_date:
                    metadata.drop(index=index, inplace=True)
        elif type == "merged":
            metadata.loc[metadata["importance"] == 1, "importance"] += 1
            metadata["importance"] -= 1

        # Get headers for the graph
        required_headers = ["ecli", "judgementdate"]
        headers = required_headers+include
        headers = list(set(headers))  # Removing duplicates.

        # Retrieve centralities data (unnormalized) and merge with corresponding ecli and importance
        centralities = pd.read_csv(self._centralities_unnormalised_path)
        data = 	pd.merge(centralities, metadata, on="ecli", how="inner")

        if "branch" in include:
            data["branch"] = self._categorise_branch_numerically(data["doctypebranch"])
        data.drop(["doctypebranch"], axis=1, inplace=True)

        # Clean columns and select only the ones that matter
        data = data[headers]
        # Drop all columns other than the ones in "include" (usually "importance" and "metric")
        [data.drop([header], axis=1, inplace=True) for header in required_headers if header not in include]
        
        return data
    
    def graph_results(self, data: pd.DataFrame, include: list, type: str) -> None:
        """
        Graph the results of the metric.

        Args:
            data (pd.DataFrame): _description_
            include (list): _description_
            type (str): _description_
        """
        metrics = [ "old_disruption", "new_disruption"]

        specifications = [("importance", "unmerged"), ("importance", "merged"), ("branch", "full")]
        for proxy, type in specifications:
            for metric in metrics:
                include = [proxy]
                include.extend([metric])
                data = self._prep_data(include, type)

                # Filter data with values of -2 (uncomputed nodes which likely have no connections)
                data = data.loc[(data[include[-1]] >= -1)]

                x_header = metric
                y_header = proxy

                x, y = list(data[x_header]), list(data[y_header])
                categories = list(set(y))
                categories.sort()
                num_categories, num_instances = len(categories), len(x)
                y_instances = [[] for category in range(num_categories)]
                for category_no in range(num_categories):
                    for instance_no in range(num_instances):
                        if y[instance_no] == category_no+1:
                            y_instances[category_no].append(x[instance_no])
                x = [statistics.mean(y_instances[category_no]) for category_no in range(num_categories)]
                y = categories

                # Draw graph
                title = f"{metric.capitalize()} vs Average {y_header.capitalize()}"
                plt.suptitle(title, fontsize=22)
                plt.xlabel(f"{metric.capitalize()}", fontsize=22)
                plt.ylabel(f"{y_header.capitalize()}", fontsize=22)
                if type == "unmerged":
                    plt.yticks([1, 2,3 , 4], label=[1, 2, 3, 4], fontsize=16)
                else:
                    plt.yticks([1, 2, 3], labels=[1, 2, 3], fontsize=16)

                # Calculate error bars
                stds = [statistics.stdev(y_instances[category_no]) for category_no in range(num_categories)]
                plt.errorbar(x, y, xerr=stds, fmt='o')

                # Save figure
                plt.savefig(self.graphs_path + f"{title}_{type}")
                #plt.show()
                plt.clf()