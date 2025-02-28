# %% IMPORTS
from datasets import load_dataset
import pandas as pd
import sqlite3
from tqdm import tqdm

# %% Load dataset metadata
input_df = pd.read_excel('data/questions-with-metadata-dataset.xlsx')

# %% Establish database connections
conn_lite = sqlite3.connect('semeval-lite.db')
conn = sqlite3.connect('semeval.db')

# %% Get unique table names from the 'dataset' column
table_names = list(input_df['dataset'].unique())

for db_conn, db_type in zip([conn_lite, conn], ["sample", "all"]):
    for name in tqdm(table_names, desc=f"Processing datasets - {db_type}"):
        try:
            # Ensure valid table names for SQLite
            table_name = name.replace("-", "_").replace(" ", "_")

            # Load the dataset
            file_path = f"hf://datasets/cardiffnlp/databench/data/{name}/{db_type}.parquet"
            df = pd.read_parquet(file_path)

            # Handle problematic column names
            rename_dict = {}
            for col in df.columns:
                if col == "airport_fee":
                    rename_dict[col] = "airport_fee_1"
                elif col == "Flash Pass Available":
                    rename_dict[col] = "Flash_Pass_Available_1"
            df.rename(columns=rename_dict, inplace=True)

            # Save to SQLite
            df.to_sql(table_name, db_conn, if_exists='replace', index=False)

        except FileNotFoundError:
            print(f"File for {name} not found. Skipping...")
        except Exception as e:
            print(f"Error processing {name}: {e}")

# Close database connections
conn_lite.close()
conn.close()
# %%