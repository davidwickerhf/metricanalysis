import sys
import os
import time
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
from utils.logger import setup_logger
from utils.timer import Timer

def main():
    """Main function to orchestrate the graph analysis tool workflow."""
    logger = setup_logger()
    timer = Timer(logger)
    
    # Step 1: Data Ingestion and Preprocessing
    logger.info("Step 1: Data Ingestion and Preprocessing")
    timer.start()
    file_reader = FileReader()
    nodes_df = file_reader.read_json('data/raw/nodes_p1.json')
    edges_df = file_reader.read_json('data/raw/edges_p1.json')
    timer.stop("Data Ingestion and Preprocessing")

    # Print the contents and columns of nodes_df to debug the KeyError
    logger.debug("Nodes DataFrame:")
    logger.debug(nodes_df.head())
    logger.debug(nodes_df.columns)

    # Print the contents and columns of edges_df to debug the KeyError
    logger.debug("Edges DataFrame:")
    logger.debug(edges_df.head())
    logger.debug(edges_df.columns)

    data_cleaner = DataCleaner()
    nodes_df = data_cleaner.remove_communicated_cases(nodes_df)
    p1_eclis = set(nodes_df['ecli'])  # Adjusted to use the correct key
    edges_df = data_cleaner.filter_targets(edges_df, p1_eclis)  # Adjusted to use the correct key

    # Save processed data
    nodes_df.to_excel('data/processed/processed_nodes.xlsx', index=False)
    edges_df.to_excel('data/processed/processed_edges.xlsx', index=False)

    # Step 2: Graph Construction
    logger.info("Step 2: Graph Construction")
    timer.start()
    graph_builder = GraphBuilder()
    G = graph_builder.create_graph(nodes_df, edges_df)
    timer.stop("Graph Construction")

    # Remove self-loops
    G.remove_edges_from(nx.selfloop_edges(G))

    # Step 3: Centrality Calculation
    logger.info("Step 3: Centrality Calculation")
    
    centrality_calculator = CentralityCalculator()
    centrality_measures = {}
    start_time = time.time()
    
    
    def log_time_and_progress(message):
        elapsed_time = time.time() - start_time
        logger.info(f"{message} (Elapsed time: {elapsed_time:.2f} seconds)")
    
    calculators = [
        ('degree_centrality', centrality_calculator.calculate_degree_centrality),
        ('in_degree_centrality', centrality_calculator.calculate_in_degree_centrality),
        ('core_number', centrality_calculator.calculate_core_number),
        ('relative_in_degree_centrality', centrality_calculator.calculate_relative_in_degree_centrality),
        ('eigenvector_centrality', centrality_calculator.calculate_eigenvector_centrality),
        ('pagerank', centrality_calculator.calculate_pagerank),
        ('current_flow_betweenness_centrality', centrality_calculator.calculate_current_flow_betweenness_centrality),
        ('forest_closeness_centrality', centrality_calculator.calculate_forest_closeness_centrality),
        ('hits', centrality_calculator.calculate_hits),
        ('trophic_level', centrality_calculator.calculate_trophic_level),
        ('betweenness_centrality', centrality_calculator.calculate_betweenness_centrality),
        ('current_flow_closeness_centrality', centrality_calculator.calculate_current_flow_closeness_centrality),
        ('out_degree_centrality', centrality_calculator.calculate_out_degree_centrality),
        ('hub_centrality', centrality_calculator.calculate_hub_centrality),
        ('authority_centrality', centrality_calculator.calculate_authority_centrality),
        ('harmonic_centrality', centrality_calculator.calculate_harmonic_centrality),
        ('disruption', centrality_calculator.calculate_disruption),
        ('closeness_centrality', centrality_calculator.calculate_closeness_centrality)
    ]

    for name, func in calculators:
        try:
            logger.info(f"Calculating {name}...")
            centrality_measures[name] = func(G)
            log_time_and_progress(f"Finished calculating {name}")
        except Exception as e:
            logger.error(f"Failed to calculate {name}: {e}")

    logger.info("All centrality calculations completed")


    for measure_name, measure_values in centrality_measures.items():
        nodes_df[measure_name] = nodes_df['ecli'].map(measure_values)  # Adjusted to use the correct key

    # Step 4: Analysis and Correlation
    logger.info("Step 4: Analysis and Correlation")
    timer.start()
    correlation_analyzer = CorrelationAnalyzer()
    centrality_columns = list(centrality_measures.keys())
    correlation_matrix = correlation_analyzer.compute_correlations(nodes_df, centrality_columns)

    composite_calculator = CompositeScoreCalculator()
    nodes_df = composite_calculator.create_composite_score(nodes_df, centrality_columns)

    regression_model = RegressionModel()
    regression_results = regression_model.perform_regression(nodes_df, 'importance')
    timer.stop("Analysis and Correlation")

    # Step 5: Visualization
    logger.info("Step 5: Visualization")
    timer.start()
    plot_generator = PlotGenerator()
    plot_generator.plot_centrality_distribution(nodes_df, 'degree_centrality')
    plot_generator.plot_correlation_matrix(correlation_matrix)

    error_bar_plotter = ErrorBarPlotter()
    error_bar_plotter.plot_error_bars(nodes_df, 'degree_centrality', 'originatingbody')
    timer.stop("Visualization")

if __name__ == "__main__":
    main()