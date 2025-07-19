# %%
import os 
from dotenv import load_dotenv
import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher
# %%
load_dotenv()

DATA_PATH = os.getenv("DATA_DIR")
print(f"DATA_PATH: {DATA_PATH}")


# %%
keywords_df = pd.read_excel(DATA_PATH + "/keywords_combined_digital/Keywords_Combined.xlsx", sheet_name="Sheet1") # type: ignore
keywords_df = keywords_df[keywords_df['yes/no'] == 'yes']
keywords_df['Keyword'] = keywords_df['Keyword'].astype(str).str.strip().str.lower()
keywords_df = keywords_df.drop(columns=['yes/no', 'Subcluster', 'Cluster'])
keywords_df['Keyword'] = (
    keywords_df['Keyword']
    .astype(str)           
    .str.strip()          
    .str.lower()          
)


companies_df = pd.read_csv(DATA_PATH + "/cb_net0_companies_concat.csv",  # type: ignore
    usecols=['org_ID', 'organisation_name', 'short_description', 'description', 'data_source'],
    dtype={'org_ID': 'string', 'organisation_name': 'string', 'short_description': 'string', 'description': 'string'},
    index_col=False)
companies_df = companies_df[companies_df['data_source'] != 'net0']

print(companies_df.shape)

# %%
companies_df['search_text'] = (
    (companies_df['short_description'].fillna('') + ' ' + companies_df['description'].fillna(''))
    .str.lower()
    .str.replace(r'[^\w\s]', ' ', regex=True)
    .str.replace(r'\s+', ' ', regex=True)
    .str.strip()
)

companies_df.drop(['short_description', 'description'], axis=1, inplace=True)

# %%
nlp = spacy.load('en_core_web_sm', disable=['ner', 'parser'])  
matcher = PhraseMatcher(nlp.vocab, attr='LEMMA')


# %%
# Extract lemmantized phrases
def lemmatize_phrase(phrase):
    # Convert a phrase to lemma form
    return ' '.join([token.lemma_ for token in nlp(phrase)])

keywords_df['Keyword_lemma'] = keywords_df['Keyword'].apply(lemmatize_phrase)
unique_lemmatized = keywords_df['Keyword_lemma'].unique()
patterns = [nlp(phrase) for phrase in unique_lemmatized]
matcher.add("KEYWORDS", patterns)

#Extract lemmatized matches from descriptions
def extract_lemmatized_matches(text):
    doc = nlp(text)
    matches = matcher(doc)
    # Get the matched span as text 
    return list(set([doc[start:end].text.lower() for _, start, end in matches]))

companies_df['matched_keywords_lemma'] = companies_df['search_text'].apply(extract_lemmatized_matches)

# %%
matches_exploded = (
    companies_df[['org_ID', 'organisation_name', 'search_text', 'matched_keywords']]
    .explode('matched_keywords')
    .dropna(subset=['matched_keywords'])
    .merge(keywords_df[['Keyword']], left_on='matched_keywords', right_on='Keyword', how='left')
)



# %%



