import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Programming Language Trends in Bioinformatics",
    page_icon="🧬",
    layout="wide"
)

# Title and subtitle
st.title("🧬 Programming Language Trends in Bioinformatics")
st.markdown("### Analysis of GitHub Repositories (2013-2025)")
st.markdown("For the github repo: [https://github.com/jpsglouzon/bio-lang-race](https://github.com/jpsglouzon/bio-lang-race)")
st.markdown("Let's chat: [https://www.biostars.org/p/9616968/](https://www.biostars.org/p/9616968/)")

# # Load data
# topic='bioinformatics'
# list_of_repos_path='../data/list_of_repos.csv' 
# stats_repo_pl_vs_topic_df_path='../data/programming_language_x_'+topic+'.csv'
# stats_repo_topics_vs_topic_df_path='../data/topics_x_'+topic+'.csv'

with st.spinner("Loading data ...", show_time=False):
    
    list_of_repos_path='https://github.com/jpsglouzon/bio-lang-race/blob/main/data/list_of_repos.csv?raw=true' 
    stats_repo_pl_vs_topic_df_path='https://github.com/jpsglouzon/bio-lang-race/blob/main/data/programming_language_x_bioinformatics.csv?raw=true'
    stats_repo_topics_vs_topic_df_path='https://github.com/jpsglouzon/bio-lang-race/blob/main/data/topics_x_bioinformatics.csv?raw=true'

    # Load datasets
    df_repos = pd.read_csv(list_of_repos_path, sep=';')
    df_lang = pd.read_csv(stats_repo_pl_vs_topic_df_path, sep=';')
    df_topics = pd.read_csv(stats_repo_topics_vs_topic_df_path, sep=';')    

# Convert topics column from string representation to actual list if needed
if 'topics' in df_repos.columns and isinstance(df_repos['topics'].iloc[0], str):
    import ast
    df_repos['topics'] = df_repos['topics'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])

# General Statistics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Repositories", f"{len(df_repos):,}")
with col2:
    st.metric("Programming Languages", f"{df_lang['language'].nunique()}")
with col3:
    st.metric("Total Stars", f"{df_repos['stars'].sum():,}")
with col4:
    st.metric("Total Forks", f"{df_repos['forks'].sum():,}")
with col5:
    st.metric("Year Range", f"{df_lang['year'].min()}-{df_lang['year'].max()}")

#     # General Statistics - Quick Overview
#     col1, col2, col3, col4 = st.columns(4)

#     # Calculate top 1 language and topic
#     top_lang_stars = df_lang.groupby('language')['stars'].sum().idxmax()
#     top_lang_forks = df_lang.groupby('language')['forks'].sum().idxmax()
#     top_topic_stars = df_topics.groupby('topic')['stars'].sum().idxmax()
#     top_topic_forks = df_topics.groupby('topic')['forks'].sum().idxmax()

#     with col1:
#         st.metric("🌟 Top Language (Stars)", top_lang_stars)
#     with col2:
#         st.metric("🔱 Top Language (Forks)", top_lang_forks)
#     with col3:
#         st.metric("🏷️ Top Topic (Stars)", top_topic_stars)
#     with col4:
#         st.metric("📌 Top Topic (Forks)", top_topic_forks)

# Sidebar filters
st.sidebar.header("🎛️ Filters")

# Get all unique languages
all_languages = sorted(df_lang['language'].unique().tolist())
default_languages = ['Python', 'C', 'C++', 'R', 'Java', 'JavaScript', 'Perl', 'Shell', 'Jupyter Notebook', 'Go']
default_languages = [lang for lang in default_languages if lang in all_languages]

selected_languages = st.sidebar.multiselect(
    "Select Programming Languages",
    options=all_languages,
    default=default_languages
)

# Year range filter
min_year = int(df_lang['year'].min())
max_year = int(df_lang['year'].max())
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Metric type
metric_type = st.sidebar.radio(
    "Select Metric Type",
    options=['stars', 'forks'],
    index=0
)

# Filter data based on selections
df_lang_filtered = df_lang[
    (df_lang['language'].isin(selected_languages)) &
    (df_lang['year'] >= year_range[0]) &
    (df_lang['year'] <= year_range[1])
]

df_topics_filtered = df_topics[
    (df_topics['year'] >= year_range[0]) &
    (df_topics['year'] <= year_range[1])
]

df_repos_filtered = df_repos[
    (df_repos['language'].isin(selected_languages)) &
    (df_repos['selected_year'] >= year_range[0]) &
    (df_repos['selected_year'] <= year_range[1])
]

# Create tabs
tab0, tab1, tab2, tab3 = st.tabs(["📋 Summary", "📈 Trends", "🔍 Pr. Languages & Topics  Comparisons", "📊 Data"])

# TAB 0: GENERAL
with tab0:
    st.header("📋 Top Languages & Topics")

    # Top 10 Languages and Topics Statistics

    col_lang, col_topic = st.columns(2)

    with col_lang:
        st.markdown("#### 🔝 Top 10 Programming Languages")

        # Calculate top 10 languages by stars
        top_10_lang_stars = df_lang.groupby('language')['stars'].sum().nlargest(10)
        total_stars = df_lang['stars'].sum()

        st.markdown("**By Stars:**")
        for i, (lang, stars) in enumerate(top_10_lang_stars.items(), 1):
            percentage = (stars / total_stars) * 100
            st.markdown(f"{i}. **{lang}**: {stars:,} stars ({percentage:.1f}%)")

        st.markdown("")

        # Calculate top 10 languages by forks
        top_10_lang_forks = df_lang.groupby('language')['forks'].sum().nlargest(10)
        total_forks = df_lang['forks'].sum()

        st.markdown("**By Forks:**")
        for i, (lang, forks) in enumerate(top_10_lang_forks.items(), 1):
            percentage = (forks / total_forks) * 100
            st.markdown(f"{i}. **{lang}**: {forks:,} forks ({percentage:.1f}%)")

    with col_topic:
        st.markdown("#### 🏷️ Top 10 Topics")

        # Calculate top 10 topics by stars
        top_10_topics_stars = df_topics.groupby('topic')['stars'].sum().nlargest(10)
        total_topic_stars = df_topics['stars'].sum()

        st.markdown("**By Stars:**")
        for i, (topic, stars) in enumerate(top_10_topics_stars.items(), 1):
            percentage = (stars / total_topic_stars) * 100
            st.markdown(f"{i}. **{topic}**: {stars:,} stars ({percentage:.1f}%)")

        st.markdown("")

        # Calculate top 10 topics by forks
        top_10_topics_forks = df_topics.groupby('topic')['forks'].sum().nlargest(10)
        total_topic_forks = df_topics['forks'].sum()

        st.markdown("**By Forks:**")
        for i, (topic, forks) in enumerate(top_10_topics_forks.items(), 1):
            percentage = (forks / total_topic_forks) * 100
            st.markdown(f"{i}. **{topic}**: {forks:,} forks ({percentage:.1f}%)")

# TAB 1: TRENDS
with tab1:
    st.header("📈 Programming Language Trends")

    # Calculate normalized percentages
    df_lang_pct = df_lang_filtered.groupby(['year', 'language'])[metric_type].sum().reset_index()
    year_totals = df_lang_pct.groupby('year')[metric_type].sum().reset_index()
    year_totals.columns = ['year', 'total']
    df_lang_pct = df_lang_pct.merge(year_totals, on='year')
    df_lang_pct['percentage'] = (df_lang_pct[metric_type] / df_lang_pct['total']) * 100

    # 1. Normalized (percentage) line chart
    st.subheader(f"💻 Normalized Percentage of {metric_type.capitalize()} by Language")
    fig1 = px.line(
        df_lang_pct,
        x='year',
        y='percentage',
        color='language',
        markers=True,
        labels={'percentage': f'Percentage of {metric_type.capitalize()} (%)', 'year': 'Year', 'language': 'Language'},
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig1.update_layout(height=500, hovermode='x unified')
    st.plotly_chart(fig1, use_container_width=True)

    # 2 & 3. Raw count and Cumulative count side by side
    col1, col2 = st.columns(2)

    # 2. Raw count line chart
    with col1:

        st.subheader(f"Raw Count of {metric_type.capitalize()} by Language")
        fig2 = px.line(
            df_lang_filtered.groupby(['year', 'language'])[metric_type].sum().reset_index(),
            x='year',
            y=metric_type,
            color='language',
            markers=True,
            labels={metric_type: f'{metric_type.capitalize()}', 'year': 'Year', 'language': 'Language'},
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig2.update_layout(height=500, hovermode='x unified')
        st.plotly_chart(fig2, use_container_width=True)

    # 3. Cumulative raw count line chart
    with col2:

        st.subheader(f"Cumulative Count of {metric_type.capitalize()} by Language")
        df_cumulative = df_lang_filtered.groupby(['year', 'language'])[metric_type].sum().reset_index()
        df_cumulative['cumulative'] = df_cumulative.groupby('language')[metric_type].cumsum()

        fig3 = px.line(
            df_cumulative,
            x='year',
            y='cumulative',
            color='language',
            markers=True,
            labels={'cumulative': f'Cumulative {metric_type.capitalize()}', 'year': 'Year', 'language': 'Language'},
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig3.update_layout(height=500, hovermode='x unified')
        st.plotly_chart(fig3, use_container_width=True)

# TAB 2: TOPICS & RACE COMPARISONS (MERGED)
with tab2:
    st.header("🔍 Programming Languages vs Topics - Comparison")

    # Side by side comparison
    st.subheader("⚖️ Language vs Topic Trends (Percentage)")

    col1, col2 = st.columns(2)

    with col1:
        # Language percentage chart
        df_lang_pct_comp = df_lang_filtered.groupby(['year', 'language'])[metric_type].sum().reset_index()
        year_totals_comp = df_lang_pct_comp.groupby('year')[metric_type].sum().reset_index()
        year_totals_comp.columns = ['year', 'total']
        df_lang_pct_comp = df_lang_pct_comp.merge(year_totals_comp, on='year')
        df_lang_pct_comp['percentage'] = (df_lang_pct_comp[metric_type] / df_lang_pct_comp['total']) * 100

        fig_lang_comp = px.line(
            df_lang_pct_comp,
            x='year',
            y='percentage',
            color='language',
            markers=True,
            title='Programming Languages (%)',
            labels={'percentage': f'% of {metric_type.capitalize()}', 'year': 'Year'},
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_lang_comp.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig_lang_comp, use_container_width=True)

    with col2:
        # Topics percentage chart
        df_topics_pct = df_topics_filtered.groupby(['year', 'topic'])[metric_type].sum().reset_index()

        # Get top 10 topics by total stars/forks
        top_topics = df_topics_pct.groupby('topic')[metric_type].sum().nlargest(10).index
        df_topics_pct = df_topics_pct[df_topics_pct['topic'].isin(top_topics)]

        year_totals_topics = df_topics_pct.groupby('year')[metric_type].sum().reset_index()
        year_totals_topics.columns = ['year', 'total']
        df_topics_pct = df_topics_pct.merge(year_totals_topics, on='year')
        df_topics_pct['percentage'] = (df_topics_pct[metric_type] / df_topics_pct['total']) * 100

        fig_topics_comp = px.line(
            df_topics_pct,
            x='year',
            y='percentage',
            color='topic',
            markers=True,
            title='Top 10 Topics (%)',
            labels={'percentage': f'% of {metric_type.capitalize()}', 'year': 'Year'},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_topics_comp.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig_topics_comp, use_container_width=True)

    st.markdown("---")

    # Race Chart Visualizations
    st.subheader("🏆 Race Chart Visualizations")

    col_race1, col_race2 = st.columns(2)

    with col_race1:
        st.markdown("##### Programming Languages Race Chart")

        # Prepare data for race chart
        df_race_lang = df_lang_filtered.groupby(['year', 'language'])[metric_type].sum().reset_index()
        df_race_lang = df_race_lang.sort_values(['year', metric_type], ascending=[True, False])

        # Get top N languages per year for animation
        top_n = 10
        df_race_lang_top = df_race_lang.groupby('year').apply(
            lambda x: x.nlargest(top_n, metric_type)
        ).reset_index(drop=True)

        fig_race_lang = px.bar(
            df_race_lang_top,
            x=metric_type,
            y='language',
            animation_frame='year',
            orientation='h',
            color='language',
            labels={metric_type: f'{metric_type.capitalize()}', 'language': 'Language'},
            range_x=[0, df_race_lang_top[metric_type].max() * 1.1],
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_race_lang.update_layout(
            height=500,
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        fig_race_lang.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 500
        st.plotly_chart(fig_race_lang, use_container_width=True)

    with col_race2:
        st.markdown("##### Topics Race Chart")

        df_race_topics = df_topics_filtered.groupby(['year', 'topic'])[metric_type].sum().reset_index()
        df_race_topics = df_race_topics.sort_values(['year', metric_type], ascending=[True, False])

        df_race_topics_top = df_race_topics.groupby('year').apply(
            lambda x: x.nlargest(top_n, metric_type)
        ).reset_index(drop=True)

        fig_race_topics = px.bar(
            df_race_topics_top,
            x=metric_type,
            y='topic',
            animation_frame='year',
            orientation='h',
            color='topic',
            labels={metric_type: f'{metric_type.capitalize()}', 'topic': 'Topic'},
            range_x=[0, df_race_topics_top[metric_type].max() * 1.1],
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_race_topics.update_layout(
            height=500,
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        fig_race_topics.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 500
        st.plotly_chart(fig_race_topics, use_container_width=True)

    st.markdown("---")

    # Top 20 repositories
    st.subheader("🌟 Top 20 Repositories by Stars/Forks")

    selected_year = st.selectbox(
        "Select Year",
        options=sorted(df_repos_filtered['selected_year'].unique(), reverse=True),
        index=0
    )

    df_top_repos = df_repos_filtered[df_repos_filtered['selected_year'] == selected_year].nlargest(20, metric_type)

    fig_top_repos = px.bar(
        df_top_repos,
        x=metric_type,
        y='name',
        orientation='h',
        color='language',
        labels={metric_type: f'{metric_type.capitalize()}', 'name': 'Repository'},
        title=f'Top 20 Repositories in {selected_year}',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_top_repos.update_layout(
        height=600,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig_top_repos, use_container_width=True)

# TAB 3: DATA
with tab3:
    st.header("📊 Dataset Explorer")

    dataset_choice = st.selectbox(
        "Select Dataset to View",
        options=['Repositories', 'Language Trends', 'Topics Trends']
    )

    if dataset_choice == 'Repositories':
        data_to_show = df_repos_filtered.copy()
        st.subheader(f"Repositories Dataset ({len(data_to_show)} records)")
    elif dataset_choice == 'Language Trends':
        data_to_show = df_lang_filtered.copy()
        st.subheader(f"Language Trends Dataset ({len(data_to_show)} records)")
    else:
        data_to_show = df_topics_filtered.copy()
        st.subheader(f"Topics Trends Dataset ({len(data_to_show)} records)")

    # Sorting options
    sort_column = st.selectbox("Sort by Column", options=data_to_show.columns.tolist())
    sort_order = st.radio("Sort Order", options=['Ascending', 'Descending'], horizontal=True)

    ascending = True if sort_order == 'Ascending' else False
    data_to_show = data_to_show.sort_values(by=sort_column, ascending=ascending)

    # Display data
    st.dataframe(data_to_show, use_container_width=True, height=500)

    # Download button
    csv = data_to_show.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Download {dataset_choice} Data as CSV",
        data=csv,
        file_name=f"{dataset_choice.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv'
    )
