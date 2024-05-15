import sys
import os
import networkx as nx

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_ingestion.reader import FileReader
from data_ingestion.cleaner import DataCleaner
from graph.builder import GraphBuilder
from centralities.calculator import CentralityCalculator
from correlation.correlation import CorrelationAnalyzer
from correlation.composite_score import CompositeScoreCalculator
from correlation.regression import RegressionModel
from visualization.plot import PlotGenerator
from visualization.error_bar import ErrorBarPlotter

def main():
    """Main function to orchestrate the graph analysis tool workflow."""
    # Step 1: Data Ingestion and Preprocessing
    file_reader = FileReader()
    nodes_df = file_reader.read_json('data/raw/nodes_p1.json')
    edges_df = file_reader.read_json('data/raw/edges_p1.json')

    # Print the contents and columns of nodes_df to debug the KeyError
    print("Nodes DataFrame:")
    print(nodes_df.head())
    print(nodes_df.columns)

    # Print the contents and columns of edges_df to debug the KeyError
    print("Edges DataFrame:")
    print(edges_df.head())
    print(edges_df.columns)

    data_cleaner = DataCleaner()
    nodes_df = data_cleaner.remove_communicated_cases(nodes_df)
    p1_eclis = set(nodes_df['ecli'])  # Adjusted to use the correct key
    edges_df = data_cleaner.filter_targets(edges_df, p1_eclis)  # Adjusted to use the correct key

    # Save processed data
    nodes_df.to_excel('data/processed/processed_nodes.xlsx', index=False)
    edges_df.to_excel('data/processed/processed_edges.xlsx', index=False)

    # Step 2: Graph Construction
    graph_builder = GraphBuilder()
    G = graph_builder.create_graph(nodes_df, edges_df)

    # Remove self-loops
    G.remove_edges_from(nx.selfloop_edges(G))

    # Step 3: Centrality Calculation
    centrality_calculator = CentralityCalculator()
    centrality_measures = {
        'degree_centrality': centrality_calculator.calculate_degree_centrality(G),
        'in_degree_centrality': centrality_calculator.calculate_in_degree_centrality(G),
        'core_number': centrality_calculator.calculate_core_number(G),
        'relative_in_degree_centrality': centrality_calculator.calculate_relative_in_degree_centrality(G),
        'eigenvector_centrality': centrality_calculator.calculate_eigenvector_centrality(G),
        'pagerank': centrality_calculator.calculate_pagerank(G),
        'current_flow_betweenness_centrality': centrality_calculator.calculate_current_flow_betweenness_centrality(G),
        'forest_closeness_centrality': centrality_calculator.calculate_forest_closeness_centrality(G),
        'hits': centrality_calculator.calculate_hits(G),
        'trophic_level': centrality_calculator.calculate_trophic_level(G),
        'betweenness_centrality': centrality_calculator.calculate_betweenness_centrality(G),
        'current_flow_closeness_centrality': centrality_calculator.calculate_current_flow_closeness_centrality(G),
        'out_degree_centrality': centrality_calculator.calculate_out_degree_centrality(G),
        'hub_centrality': centrality_calculator.calculate_hub_centrality(G),
        'authority_centrality': centrality_calculator.calculate_authority_centrality(G),
        'harmonic_centrality': centrality_calculator.calculate_harmonic_centrality(G),
        'disruption': centrality_calculator.calculate_disruption(G),
        'closeness_centrality': centrality_calculator.calculate_closeness_centrality(G),
    }

    for measure_name, measure_values in centrality_measures.items():
        nodes_df[measure_name] = nodes_df['ecli'].map(measure_values)  # Adjusted to use the correct key

    # Step 4: Analysis and Correlation
    correlation_analyzer = CorrelationAnalyzer()
    centrality_columns = list(centrality_measures.keys())
    correlation_matrix = correlation_analyzer.compute_correlations(nodes_df, centrality_columns)

    composite_calculator = CompositeScoreCalculator()
    nodes_df = composite_calculator.create_composite_score(nodes_df, centrality_columns)

    regression_model = RegressionModel()
    regression_results = regression_model.perform_regression(nodes_df, 'importance')

    # Step 5: Visualization
    plot_generator = PlotGenerator()
    plot_generator.plot_centrality_distribution(nodes_df, 'degree_centrality')
    plot_generator.plot_correlation_matrix(correlation_matrix)

    error_bar_plotter = ErrorBarPlotter()
    error_bar_plotter.plot_error_bars(nodes_df, 'degree_centrality', 'originatingbody')

if __name__ == "__main__":
    main()