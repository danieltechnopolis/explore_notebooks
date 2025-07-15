# %%
import os 
from dotenv import load_dotenv
import pandas as pd

# %%
load_dotenv()
DATA_PATH = os.getenv("DATA_DIR")
print(f"DATA_PATH: {DATA_PATH}")


data_path_1 = os.path.join(DATA_PATH, 'digital_sectors_merge/EU_Digital_Sectors_20250604.xlsx')
data_path_2 = os.path.join(DATA_PATH, 'cb_net0_companies_concat.csv')
save_path = os.path.join(DATA_PATH, 'digital_sectors_merge/merged_data_digital_sectors.xlsx')

# %%
df_full = pd.read_csv(data_path_2)
df_tech = pd.read_excel(data_path_1, sheet_name='Companies')
print(df_full.shape, df_tech.shape)


# %%
df_tech = df_tech.rename(columns={'crunchbase_url': 'cb_url'})
df_tech = df_tech[df_tech['cb_url'].notna()]
df_tech['cb_url'] = df_tech['cb_url'].astype(str)

# %%
df_tech['cb_url'] = (
    df_tech['cb_url']
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace('https://', '', regex=False)
    .str.replace('http://', '', regex=False)
    .str.replace('www.', '', regex=False)
)

df_full['cb_url'] = (
    df_full['cb_url']
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace('https://', '', regex=False)
    .str.replace('http://', '', regex=False)
    .str.replace('www.', '', regex=False)
)

# %%

df_full_reduced = (
    df_full[['cb_url', 'email', 'phone']]
    .drop_duplicates(subset='cb_url', keep='first')
)
df_tech = df_tech[df_tech['cb_url'].notna()]
df_full_reduced = df_full_reduced[df_full_reduced['cb_url'].notna()]



# %%

df_merged = df_tech.merge(df_full_reduced, on='cb_url', how='inner')
print(f"Merged count: {len(df_merged)}")
print("df_tech rows:", len(df_tech))
print("Merged rows:", len(df_merged))
df_tech[~df_tech['cb_url'].isin(df_merged['cb_url'])]

# %%
df_merged.to_excel(save_path, index=False)


