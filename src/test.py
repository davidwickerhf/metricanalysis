import pandas as pd

file_path = 'data/raw/nodes_p1.json'
file_2 = 'data/raw/edges_p1.json'

# nodes_df = pd.read_json(file_path)
# print(nodes_df.head())
# print(nodes_df.columns)

edges_df = pd.read_json(file_2)
print(edges_df.head())
print(edges_df.columns)
