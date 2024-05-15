from src.data_ingestion.reader import FileReader
from src.data_ingestion.cleaner import DataCleaner
from src.graph.builder import GraphBuilder
from src.centralities.calculator import CentralityCalculator
from src.correlation.correlation import CorrelationAnalyzer
from src.correlation.composite_score import CompositeScoreCalculator
from src.correlation.regression import RegressionModel
from src.visualization.plot import PlotGenerator
from src.visualization.error_bar import ErrorBarPlotter

def main():
    """Main function to orchestrate the graph analysis tool workflow."""
    # Step 1: Data Ingestion and Preprocessing
    file_reader = FileReader()
    nodes_df = file_reader.read_json('data/raw/nodes_p1.json')
    edges_df = file_reader.read_json('data/raw/edges_p1.json')

    data_cleaner = DataCleaner()
    nodes_df = data_cleaner.remove_communicated_cases(nodes_df)
    p1_eclis = set(nodes_df['ECLI'])
    edges_df = data_cleaner.filter_targets(edges_df, p1_eclis)

    # Save processed data
    nodes_df.to_excel('data/processed/processed_nodes.xlsx', index=False)
    edges_df.to_excel('data/processed/processed_edges.xlsx', index=False)

    # Step 2: Graph Construction
    graph_builder = GraphBuilder()
    G = graph_builder.create_graph(nodes_df, edges_df)

    # Step 3: Centrality Calculation
    centrality_calculator = CentralityCalculator()
    degree_centrality = centrality_calculator.calculate_degree_centrality(G)
    betweenness_centrality = centrality_calculator.calculate_betweenness_centrality(G)
    # Add more centrality measures as needed

    # Add centrality measures to nodes_df
    nodes_df['degree_centrality'] = nodes_df['ECLI'].map(degree_centrality)
    nodes_df['betweenness_centrality'] = nodes_df['ECLI'].map(betweenness_centrality)

    # Step 4: Analysis and Correlation
    correlation_analyzer = CorrelationAnalyzer()
    correlation_matrix = correlation_analyzer.compute_correlations(nodes_df, ['degree_centrality', 'betweenness_centrality'])

    composite_calculator = CompositeScoreCalculator()
    nodes_df = composite_calculator.create_composite_score(nodes_df, ['degree_centrality', 'betweenness_centrality'])

    regression_model = RegressionModel()
    regression_results = regression_model.perform_regression(nodes_df, 'importance_score')

    # Step 5: Visualization
    plot_generator = PlotGenerator()
    plot_generator.plot_centrality_distribution(nodes_df, 'degree_centrality')
    plot_generator.plot_correlation_matrix(correlation_matrix)

    error_bar_plotter = ErrorBarPlotter()
    error_bar_plotter.plot_error_bars(nodes_df, 'degree_centrality', 'court_branch')

if __name__ == "__main__":
    main()
