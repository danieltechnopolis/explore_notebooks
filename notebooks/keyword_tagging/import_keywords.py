import pandas as pd  # noqa: F401
import re




def extract_keywords(
    df,  
    industry_col,              
    transition_col='Transition',
    technology_col='Technology'
):
    """
    Extracts keywords from a specified industry column in a DataFrame.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data.

    industry_col : str
        Name of the industry column to extract keywords from.

    transition_col : str
        Name of the transition column.
        
    technology_col : str
        Name of the technology column.
    
    Returns
    -------
    pd.DataFrame with columns: Transition, Technology, associated keywords.
    """

    
    # Only keep rows where there are actual keywords in the specified industry column
    df = df[df[industry_col].notna() & (df[industry_col].astype(str).str.strip() != '')]
    tidy_df = (
        df
        .assign(**{industry_col: df[industry_col].astype(str).str.split(',')})
        .explode(industry_col)
        .assign(**{industry_col: lambda d: d[industry_col].str.strip()})
        .rename(columns={

            transition_col: 'transition',
            technology_col: 'technology',
            industry_col: 'keywords'

        })
        .loc[:, ['transition', 'technology', 'keywords']]
        .reset_index(drop=True)
    )

    tidy_df['keywords'] = tidy_df['keywords'].str.replace('"', '', regex=False).str.replace("'", '', regex=False).str.strip()
    return tidy_df



def clean_text(text):

    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)   # Replace all punctuation with space
    text = re.sub(r'\s+', ' ', text)       # Collapse multiple spaces/newlines to one space
    return text.strip()



def find_matched_keywords(row, keywords):

    text = row.lower()
    matched_keywords = [
        kw for kw in keywords
        if re.search(r'\b{}\b'.format(re.escape(kw.lower())), text)
    ]
    return ", ".join(sorted(set(matched_keywords)))



def match_technologies(text, kw_dict):

    text = text.lower()
    matches = []
    for kw, tech in kw_dict.items():
        pattern = r'(?<!\w){}(?!\w)'.format(re.escape(kw))
        if re.search(pattern, text):
            matches.append(tech)
    return ', '.join(sorted(set(matches)))



def find_keywords_from_df(text, keyword_df):
    """
    Matches keywords from DataFrame to search text.
    Returns the unique categories associated with any matches.
    """

    matched_categories = (
        keyword_df[keyword_df.iloc[:,2].apply(lambda k: re.search(rf'\b{re.escape(str(k))}\b', str(text), re.IGNORECASE) is not None)]
        .iloc[:,1]
        .unique()
    )
    return ", ".join([cat.strip() for cat in matched_categories])




def normalize_text(text):
    if pd.isnull(text):
        return ""

    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text