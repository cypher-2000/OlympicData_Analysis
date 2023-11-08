import pandas as pd


def preprocess(df, region_df):
    # global df, region_df

    df = df[df['Season'] == 'Summer']

    merged_df = df.merge(region_df, on='NOC', how='left')

    merged_df.drop_duplicates(inplace=True)

    merged_df = pd.concat([merged_df, pd.get_dummies(merged_df['Medal'])], axis=1)
    # print(merged_df.columns)
    return merged_df

# preprocess()
