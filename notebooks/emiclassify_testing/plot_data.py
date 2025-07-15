import os 
from dotenv import load_dotenv
import matplotlib.pyplot as plt  # noqa: F401
import pandas as pd
import numpy as np # noqa: F401
from precision_recall import plot_confusion_by_sector




load_dotenv()

DATA_PATH = os.getenv("PROJECT_DATA_PATH")

file_path = os.path.join(DATA_PATH, 'sample_test_3ecsytm.xlsx') # type: ignore


xls = pd.ExcelFile(file_path)
dfs = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
agri_df = dfs['Agrifood']
tourism_df = dfs['Tourism']
textile_df = dfs['Textiles']



sectors = {
    'Agrifood': agri_df,
    'Tourism': tourism_df,
    'Textiles': textile_df
}


sector_label_map = {
    'Agrifood': {'Agrifood': 1, 'Tourism': 0, 'Textiles': 0},
    'Tourism':  {'Agrifood': 0, 'Tourism': 1, 'Textiles': 0},
    'Textiles': {'Agrifood': 0, 'Tourism': 0, 'Textiles': 1}
}




# Plotting all bar plots together for easy comparison
for sector, df in sectors.items():
    label_df = df[['org_ID', 'answer', 'source']]
    plot_confusion_by_sector(label_df, sector, sector_label_map[sector]) 