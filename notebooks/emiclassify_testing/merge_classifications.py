import os 
from dotenv import load_dotenv
import pandas as pd




load_dotenv()

DATA_PATH = os.getenv("PROJECT_DATA_PATH")
if DATA_PATH is None:
	raise ValueError("PROJECT_DATA_PATH is not set.")

file_path = os.path.join(DATA_PATH, '')

df_prob_path = os.path.join(file_path, 'Aerospace & Defence_batch_P_results.xlsx')
df_binary_path = os.path.join(file_path, 'Aerospace & Defence_batch_results.xlsx')


df_prob = pd.read_excel(df_prob_path)
df_binary = pd.read_excel(df_binary_path)


merged_df = pd.merge(
    df_binary,
    df_prob[['org_ID', 'Probability']],
    on='org_ID',
    how='left'
)

order = ['Probability', 'answer'] + [col for col in merged_df.columns if col not in ['Probability', 'answer']]
merged_df = merged_df[order]

merged_df[merged_df['Probability'] >= 0.6]



