import sys
import os
import time
import networkx as nx
import pandas as pd



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
            measure_values = func(G)
            centrality_measures[name] = measure_values
            log_time_and_progress(f"Finished calculating {name}")
        except Exception as e:
            logger.error(f"Failed to calculate {name}: {e}")

    logger.info("All centrality calculations completed")

    # Adding the centrality measures to the nodes DataFrame
    for measure_name, measure_values in centrality_measures.items():
        try:
            logger.info(f"Mapping {measure_name} to nodes DataFrame")
            nodes_df[measure_name] = nodes_df['ecli'].map(measure_values)  # Ensure measure_values is a dictionary
        except Exception as e:
            logger.error(f"Failed to map {measure_name} to nodes DataFrame: {e}")

    # Save the updated DataFrame
    nodes_df.to_excel('data/processed/processed_nodes.xlsx', index=False)
    logger.info("Saved the processed nodes DataFrame to Excel")

    # Correlation analysis
    correlation_analyzer = CorrelationAnalyzer()
    centrality_columns = [col for col in nodes_df.columns if col not in ['ecli', 'court_branch', 'importance']]
    
    try:
        correlation_matrix = correlation_analyzer.compute_correlations(nodes_df, centrality_columns)
        correlation_matrix.to_excel('data/processed/correlation_matrix.xlsx')
        logger.info("Correlation matrix computed and saved.")
    except Exception as e:
        logger.error(f"Failed to compute correlation matrix: {e}")

    # Correlation with importance
    try:
        importance_correlations = correlation_analyzer.compute_importance_correlations(nodes_df, centrality_columns)
        importance_correlations.to_excel('data/processed/importance_correlations.xlsx')
        logger.info("Importance correlations computed and saved.")
    except Exception as e:
        logger.error(f"Failed to compute importance correlations: {e}")

    # Correlation with court branch
    try:
        court_branch_correlations = correlation_analyzer.compute_court_branch_correlations(nodes_df, centrality_columns)
        court_branch_correlations.to_excel('data/processed/court_branch_correlations.xlsx')
        logger.info("Court branch correlations computed and saved.")
    except Exception as e:
        logger.error(f"Failed to compute court branch correlations: {e}")

    # Select numeric columns for regression analysis
    numeric_df = nodes_df.select_dtypes(include=[float, int])

    # Check if the target column 'importance' is numeric
    if 'importance' not in numeric_df.columns:
        try:
            numeric_df['importance'] = pd.to_numeric(nodes_df['importance'], errors='coerce')
        except Exception as e:
            logger.error(f"Failed to convert 'importance' to numeric: {e}")
            return

    # Drop rows with NaN values in the target column
    numeric_df = numeric_df.dropna(subset=['importance'])

    # Save the processed nodes data
    try:
        nodes_df.to_excel('data/processed/processed_nodes.xlsx', index=False)
        logger.info("Processed nodes data saved.")
    except Exception as e:
        logger.error(f"Failed to save processed nodes data: {e}")

    end_time = time.time()
    logger.info(f"Execution completed in {end_time - start_time:.2f} seconds.")

    # TODO - Implement composite score
    # composite_calculator = CompositeScoreCalculator()
    # nodes_df = composite_calculator.create_composite_score(nodes_df, centrality_columns)

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