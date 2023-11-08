import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
from plotly.figure_factory import create_distplot

import helper
import preprocess

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

# Load data and preprocess it
merged_df = preprocess.preprocess(df, region_df)

st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
st.sidebar.title("Olympic Data Analysis")
# Create a Streamlit radio button to select an option
user_menu = st.sidebar.radio(
    'Select an Option', ('Medal Analysis', 'Overall Analysis', 'Athlete-wise Analysis', 'Country-wise Analysis')
)

if user_menu == 'Medal Analysis':
    # st.sidebar.image('https://library.sportingnews.com/styles/crop_style_16_9_desktop_webp/s3/2022-01/Beijing-Olympic-medals-013122-Getty-FTR.jpg.webp?itok=Or24kllB')
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(merged_df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally_x, medal_tally_y, flag = helper.fetch_medal_tally(merged_df, selected_year, selected_country)

    # Display x and y DataFrames in separate components
    if selected_year == 'Overall' and selected_country == 'Overall':
        # st.image(
        #     'https://library.sportingnews.com/styles/crop_style_16_9_desktop_webp/s3/2022-01/Beijing-Olympic-medals-013122-Getty-FTR.jpg.webp?itok=Or24kllB')
        st.subheader("Overall Medal Tally")
        st.table(medal_tally_x)

    if selected_year == 'Overall' and selected_country != 'Overall':
        st.subheader("Overall Medal Tally of " + selected_country)
        st.table(medal_tally_x)

    if selected_year != 'Overall' and selected_country != 'Overall':
        st.subheader(selected_country + "'s performance in " + str(selected_year) + " Olympics")
        st.table(medal_tally_x)

    if selected_year != 'Overall' and selected_country == 'Overall':
        st.subheader("Overall performance of all countries in " + str(selected_year))
        st.table(medal_tally_x)
    # st.subheader("Medal Tally for Selected Country (Overall)")
    # st.dataframe(medal_tally_y)

    if flag == 1 and medal_tally_y is not None:  # Check if flag is 1 and medal_tally_y is not None
        st.subheader("Overall total Medals of " + selected_country)
        assert isinstance(medal_tally_y, object)
        st.table(medal_tally_y)

# ///Overall Analysis


if user_menu == "Overall Analysis":
    editions = merged_df['Year'].unique().shape[0] - 1
    cities = merged_df['City'].unique().shape[0]
    sports = merged_df['Sport'].unique().shape[0]
    events = merged_df['Event'].unique().shape[0]
    athletes = merged_df['Name'].unique().shape[0]
    nations = merged_df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)

    col3, col4 = st.columns(2)
    with col3:
        st.header("Sports")
        st.title(sports)

    with col4:
        st.header("Events")
        st.title(events)

    col5, col6 = st.columns(2)
    with col5:
        st.header("Athletes")
        st.title(athletes)
    with col6:
        st.header("Nations")
        st.title(nations)

    # nan_count = merged_df.isna().sum()
    # print("NaN count in merged_df:")
    # print(nan_count)

    # if user_menu == "Overall Analysis":

    nations_over_time = helper.data_over_time(merged_df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)
    # assert isinstance(nations_over_time.columns, object)
    # print(nations_over_time)

    events_over_time = helper.data_over_time(merged_df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(merged_df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(15, 15))
    x = merged_df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

    #     data = helper.most_successful(merged_df,'Overall')
    # # print(data)
    #     st.table(data)

    st.title("Most successful Athletes")
    sport_list = merged_df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(merged_df, selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    country_list = merged_df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(merged_df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + "'s Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(merged_df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(merged_df, selected_country)
    st.table(top10_df)

# country_df = helper.yearwise_medal_tally(merged_df,'USA')
# print(country_df)

############

    year_list = merged_df['Year'].unique().tolist()
    year_list.sort()
    st.title("Medal Table")
    selected_year = st.selectbox('Select a Year', year_list)
    st.title(selected_country + "'s medals in " + str(selected_year))

    temp_df= helper.get_medalists_by_year_and_country(merged_df,selected_country,selected_year)
    st.table(temp_df)


if user_menu == 'Athlete-wise Analysis':
    athlete_df = merged_df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.title("Distribution of Age wrt Sports(Silver Medalist)")
    st.plotly_chart(fig)
    #
    # for sport in famous_sports:
    #     temp_df = athlete_df[athlete_df['Sport'] == sport]
    #     x.append(temp_df[temp_df['Medal'] == 'Bronze']['Age'].dropna())
    #     name.append(sport)
    #
    # fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    # fig.update_layout(autosize=False, width=800, height=600)
    # st.title("Distribution of Age wrt Sports(Bronze Medalist)")
    # st.plotly_chart(fig)
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        bronze_age_data = temp_df[temp_df['Medal'] == 'Bronze']['Age'].dropna()

        if not bronze_age_data.empty:
            x.append(bronze_age_data)
            name.append(sport)

    if x:  # Check if x is not empty before creating the plot
        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=800, height=600)
        st.title("Distribution of Age wrt Sports (Bronze Medalist)")
        st.plotly_chart(fig)
    else:
        st.warning("No data available for Bronze Medalists in the selected sports.")

    # data = helper.men_vs_women(merged_df)
    # print(data)

    sport_list = merged_df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    # st.title('Height Vs Weight')
    # selected_sport = st.selectbox('Select a Sport', sport_list)
    # temp_df = helper.weight_v_height(merged_df,selected_sport)
    # fig,ax = plt.subplots()
    # ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    # st.pyplot(fig)

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(merged_df, selected_sport)

    fig, ax = plt.subplots(figsize=(10, 6))  # Create a figure and axis

    sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=60, ax=ax)
    ax.set_title('Height Vs Weight')
    ax.set_xlabel('Weight')
    ax.set_ylabel('Height')

    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(merged_df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=800, height=600)
    st.plotly_chart(fig)
