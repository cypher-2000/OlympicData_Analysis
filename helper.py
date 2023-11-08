# def medal_tally(merged_df):
#     medal_tally = merged_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Medal', 'Event'])
#
#     medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
#                                                                                                 ascending=False).reset_index()
#
#     medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
#
#     return medal_tally
import numpy as np


def medal_tally1(merged_df):
    medal_tally1 = merged_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Medal', 'Event'])

    medal_tally1 = medal_tally1.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                  ascending=False).reset_index()

    medal_tally1['Total'] = medal_tally1['Gold'] + medal_tally1['Silver'] + medal_tally1['Bronze']
    # print(medal_tally1.columns)
    return medal_tally1


# medal_tally(merged_df)

def country_year_list(merged_df):
    years = merged_df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(merged_df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def fetch_medal_tally(merged_df, years, country):
    medal_df = merged_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Medal', 'Event'])
    flag = 0
    if years == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if years == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if years != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(years)]
    if years != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == years)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
        # x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
        y = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()
        y['Total'] = y['Gold'] + y['Silver'] + y['Bronze']
        return x, y, flag
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x, None, flag


### overall Analysis

def data_over_time(merged_df, col):
    nations_over_time = merged_df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values(
        'Year')
    nations_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    return nations_over_time


# def most_successful(merged_df, sport):
#     temp_df = merged_df.dropna(subset=['Medal'])
#
#     if sport != 'Overall':
#         temp_df = temp_df[temp_df['Sport'] == sport]
#     x = temp_df['Name'].value_counts().reset_index().head(15)
#     y = x.merge(merged_df,left_on='Name', right_on='count', how='left')
#     # x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
#     #     ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
#     # x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
#     return y

def most_successful(merged_df, sport):
    temp_df = merged_df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Group by 'Name' and count the number of occurrences
    x = temp_df['Name'].value_counts().reset_index().head(30)
    x.columns = ['Name', 'Medals']

    # Merge with 'merged_df' using the 'Name' column
    y = x.merge(merged_df, on='Name', how='left')[['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name')

    return y


def yearwise_medal_tally(merged_df, country):
    temp_df = merged_df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def country_event_heatmap(merged_df, country):
    temp_df = merged_df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(merged_df, country):
    temp_df = merged_df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(15)
    x.columns = ['Name', 'Medals']

    # Merge with 'merged_df' using the 'Name' column
    y = x.merge(merged_df, on='Name', how='left')[['Name', 'Medals', 'Sport']].drop_duplicates('Name')

    # x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
    #     ['index', 'Name_x', 'Sport']].drop_duplicates('index')
    # x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return y


def weight_v_height(merged_df, sport):
    athlete_df = merged_df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df



def get_medalists_by_year_and_country(merged_df, country, year):
    # Filter the DataFrame for the given country and year
    filtered_df = merged_df[(merged_df['region'] == country) & (merged_df['Year'] == year)]

    # Filter for rows with non-null 'Medal' values
    filtered_df = filtered_df.dropna(subset=['Medal'])

    # Select relevant columns
    relevant_columns = ['Name', 'Sport', 'Medal']

    # Extract the medalists' information
    medalists_info = filtered_df[relevant_columns]

    return medalists_info

def men_vs_women(merged_df):
    athlete_df = merged_df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
