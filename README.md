# Metrics Tool

## Introduction

Metrics Tool is a Python package and CLI (Command-Line Interface) tool designed to facilitate the testing of various graph metrics on input datasets. It streamlines the process of evaluating graph metrics by allowing users to input a CSV file of nodes and another CSV file of edges, and then compare the computed metrics against a set of ground truths. This tool is ideal for researchers, data scientists, and anyone interested in graph analysis and performance measurement.

## Features

- **Custom Metric Evaluation:** Apply and test custom graph metrics on your datasets.
- **Ground Truth Comparison:** Analyze the performance of graph metrics by comparing them with ground truths.
- **CLI and Library Support:** Use Metrics Tool as a command-line tool or as a Python library in your projects.
- **Extensive Documentation:** Get started quickly with our detailed guides and examples.

## Supported Metrics

The Metrics Tool currently supports the following metrics:

- **Degree**: Measures the number of connections a node has.
- **In-degree**: Counts the number of inward edges a node has.
- **Core Number**: Identifies the maximal subgraph in which each node has a degree greater than or equal to the core number.
- **Relative In-degree**: A normalized version of in-degree, considering the total number of nodes.
- **Eigenvector**: Reflects the influence of a node in a network.
- **PageRank**: Evaluates the importance of nodes based on the link structure.
- **Current Flow Betweenness**: A variant of betweenness centrality that uses electrical current flow models as proxies.
- **Forest Closeness**: An adaptation of closeness centrality that takes forest structures into account.
- **HITS**: Determines hubs and authorities in a network using the hyperlink-induced topic search algorithm.
- **Trophic Level**: Measures the position of a node in a trophic hierarchy.
- **Betweenness**: Quantifies the number of times a node acts as a bridge along the shortest path between two other nodes.
- **Current Flow Closeness**: A centrality measure using network flow to assess node closeness.
- **Out-degree**: The number of outgoing connections from a node.
- **Hub**: Identifies hub nodes within a network.
- **Authority**: Identifies nodes with authoritative sources of information.
- **Harmonic**: Measures node centrality based on the harmonic mean distance to other nodes.
- **Disruption**: Assesses the impact of a node's removal on network performance.
- **Closeness**: The average length of the shortest path from the node to all other nodes.

## File Structure

- **edges.csv**: This file contains two columns: `ecli` and `references`. Each row represents an edge, with `ecli` indicating the case identifier and `references` being a list of case identifiers that the `ecli` case references.
  
  Example row: `ECLI:CE:ECHR:1968:0627JUD000193663,"['ECLI:CE:ECHR:1960:1114JUD000033257', 'ECLI:CE:ECHR:1961:0701JUD000033257', 'ECLI:CE:ECHR:1961:0407JUD000033257']"`

- **nodes.csv**: This file contains details about each node. The columns are as follows: `ecli`, `itemid`, `appno`, `article`, `conclusion`, `docname`, `doctype`, `doctypebranch`, `importance`, `judgementdate`, `languageisocode`, `originatingbody`, `violation`, `nonviolation`, `extractedappno`, `scl`.

- **ground_truths.csv**: The structure for this file should include the ground truths against which the metrics will be compared. The structure depends on what ground truths are required for the supported metrics.

## Project Folder Structure

The project is organized into the following structure:

- **.env/**: Environment configuration files for local development.
- **docs/**: Documentation files and additional resources.
- **metrics/**:
  - **cli/**:
    - **metrics.py**: The CLI interface for running the tool.
  - **functions/**:
    - **metric.py**: Function definitions for each metric supported by the tool.
  - **util/**:
    - **timer.py**: Utility functions for timing and performance measurement.
    - **__init__.py**: Initializes the `metrics` package.
- **tests/**: Contains unit tests for each metric and utility function.
- **.gitattributes**: Git configuration file for handling repository attributes.
- **.gitignore**: Specifies intentionally untracked files to ignore.
- **LICENSE**: The full license text.
- **README.md**: The file you are currently reading.
- **requirements.txt**: Lists all Python dependencies.
- **setup.py**: Configuration for packaging and distributing the tool.

## Future TO-Dos

- **Improve Documentation**: Continually update and expand the documentation to cover all aspects of the tool, including more detailed usage examples.
- **Add Unit Testing**: Develop a comprehensive suite of unit tests to ensure each metric's accuracy and reliability.
- **Add Support for Custom Metrics and Ground Truths**: Implement a flexible system to allow users to define and

 integrate their custom metrics and ground truths into the tool.


## Installation

To install Metrics Tool, you need Python 3.6 or later. You can install it using pip:

```bash
pip install metricstool
```

## Quick Start

### As a CLI Tool

1. **Prepare Your Datasets:** Ensure you have two CSV files: one for nodes and another for edges. 

    Example:
    - `nodes.csv`: Contains the nodes of your graph.
    - `edges.csv`: Contains the edges connecting the nodes in your graph.

2. **Run Metrics Tool:** Use the following command to run Metrics Tool against your datasets.

    ```bash
    metricstool --nodes nodes.csv --edges edges.csv --metrics your_metric --ground-truths ground_truths.csv
    ```

    Replace `your_metric` with the metric you wish to test and `ground_truths.csv` with the path to your ground truths file.

### As a Python Package

1. **Import Metrics Tool:**

    ```python
    from metricstool import MetricsTool
    ```

2. **Load Your Datasets:**

    ```python
    nodes_path = 'path/to/nodes.csv'
    edges_path = 'path/to/edges.csv'
    ground_truths_path = 'path/to/ground_truths.csv'
    ```

3. **Initialize and Run Metrics Tool:**

    ```python
    mt = MetricsTool(nodes_path, edges_path)
    results = mt.evaluate_metric('your_metric', ground_truths_path)
    print(results)
    ```

## Documentation

- **Getting Started:** A guide to get you started with Metrics Tool quickly.
- **API Reference:** Detailed description of the API, parameters, and return types.
- **Examples:** Various examples to illustrate how to use Metrics Tool effectively.
- **FAQs:** Answers to common questions and issues.

## Support

If you encounter any issues or have questions, please file an issue on our GitHub repository.
