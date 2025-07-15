import pandas as pd





def df_summary(df, column):

    if isinstance(column, str):
        column = [column]
    
    summary_list = []

    for col in column:
        counts = df[col].value_counts(dropna=False)
        percents = df[col].value_counts(normalize=True, dropna=False).mul(100).round(2)
        temp_df = (
            pd.DataFrame({ 
                'column': col,
                'value': counts.index,
                'count': counts.values,
                'percent': percents.values
            })
        )
        summary_list.append(temp_df)
    
    # Concatenate all column summaries
    summary_df = pd.concat(summary_list, ignore_index=True)
    return summary_df




def reorder_columns(df, new_order):
    # Only keep columns that exist in both df and new_order
    cols_to_use = [col for col in new_order if col in df.columns]
    return df[cols_to_use]




def make_val_data(dfs, n, source=None):

    if source is None:
        source = [f'source_{i}' for i in range(len(dfs))]

    sampled_dfs = [
        df.sample(n=n, random_state=42).assign(source=src)
        for df, src in zip(dfs, source)
    ]
    val_data = pd.concat(sampled_dfs, ignore_index=True)
    return val_data

