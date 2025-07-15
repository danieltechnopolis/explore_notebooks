import os
from  dotenv import load_dotenv
import pandas as pd
from summarise import make_val_data




load_dotenv()



DATA_PATH = os.getenv('COMPANY_DATA_PATH')
if DATA_PATH is None:
    raise ValueError("COMPANY_DATA_PATH environment variable is not set.")



agrifood_path = os.path.join(DATA_PATH, 'Agrifood.xlsx')

textile_path = os.path.join(DATA_PATH, 'Textiles.xlsx')

tourism_path = os.path.join(DATA_PATH, 'Tourism.xlsx')



# Load the data from the Excel files
agri_df = pd.read_excel(agrifood_path)

textile_df = pd.read_excel(textile_path)

tourism_df = pd.read_excel(tourism_path)



# Combine the dataframes into a list
dfs = [agri_df, textile_df, tourism_df]

val_data = make_val_data(dfs, n=500, source=['Agrifood', 'Textiles', 'Tourism'])



# Save the validation data to a CSV file
val_data_path = os.path.join(DATA_PATH, 'validation_data.csv')

val_data.to_csv(val_data_path, index=False)










