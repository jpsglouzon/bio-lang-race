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
st.markdown("Github repo: [https://github.com/jpsglouzon/bio-lang-race](https://github.com/jpsglouzon/bio-lang-race)")
st.markdown("Let's chat: [Biostar](https://www.biostars.org/p/9616968/) & [r/bioinformatics](https://www.reddit.com/r/bioinformatics/comments/1q1ulir/analyzing_15_years_of_bioinformatics_how/)")

# # Load data
# topic='bioinformatics'
# list_of_repos_path='../data/list_of_repos_'+topic+'.csv'
# stats_repo_pl_vs_topic_df_path='../data/programming_language_x_'+topic+'.csv'
# stats_repo_topics_vs_topic_df_path='../data/topics_x_'+topic+'.csv'

with st.spinner("Loading data ...", show_time=False):
    
    list_of_repos_path='https://github.com/jpsglouzon/bio-lang-race/blob/main/data/list_of_repos_bioinformatics.csv?raw=true' 
    stats_repo_pl_vs_topic_df_path='https://github.com/jpsglouzon/bio-lang-race/blob/main/data/programming_language_x_bioinformatics.csv?raw=true'
    stats_repo_topics_vs_topic_df_path='https://github.com/jpsglouzon/bio-lang-race/blob/main/data/topics_x_bioinformatics.csv?raw=true'

    # Load datasets
    df_repos = pd.read_csv(list_of_repos_path, sep=';',header=0,on_bad_lines='skip')
    df_lang = pd.read_csv(stats_repo_pl_vs_topic_df_path, sep=';',header=0)
    df_topics = pd.read_csv(stats_repo_topics_vs_topic_df_path, sep=';',header=0)    

# Convert topics column from string representation to actual list if needed
if 'topics' in df_repos.columns and isinstance(df_repos['topics'].iloc[0], str):
    import ast
    df_repos['topics'] = df_repos['topics'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])
    
    
# Calculate top 1 language and topic
top_lang_stars = df_lang.groupby('language')['stars'].sum().idxmax()
top_lang_forks = df_lang.groupby('language')['forks'].sum().idxmax()
top_topic_stars = df_topics.groupby('topic')['stars'].sum().idxmax()
top_topic_forks = df_topics.groupby('topic')['forks'].sum().idxmax()    

# General Statistics
col1, col2, col3, col4, col5, col6, col7= st.columns(7)

with col1:
    st.metric(label="🌟 Top Language (Stars)", value=top_lang_stars,delta='Forks: '+top_lang_forks,delta_color='off')

with col2:
    st.metric("🏷️ Top Topic (Stars)", top_topic_stars,delta='Forks: '+top_topic_forks,delta_color='off')
    
with col3:
    st.metric("Total Repositories", f"{len(df_repos):,}")
with col4:

    st.metric("Programming Languages", f"{df_lang['language'].nunique()}")
with col5:
    st.metric("Total Stars", f"{df_repos['stars'].sum():,}")
with col6:
    st.metric("Total Forks", f"{df_repos['forks'].sum():,}")
with col7:
    st.metric("Year Range", f"{df_lang['year'].min()}-{df_lang['year'].max()}")



#     # General Statistics - Quick Overview
#     col1, col2, col3, col4 = st.columns(4)


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
tab0, tab1, tab2, tab3 = st.tabs(["📋 Summary", "📈 Programming Language and Topics Trends", "🌟 Top 20 Repositories", "📊 Data"])

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
    st.header("📈 Programming Language and Topics Trends")


    col1, col2 = st.columns(2)

    with col1:

        # Language rank chart
        df_lang_rank_comp = df_lang_filtered.groupby(['year', 'language'])[metric_type].sum().reset_index()
        
        # Calculate rank for each year - rank 1 = highest stars/forks
        df_lang_rank_comp['rank'] = df_lang_rank_comp.groupby('year')[metric_type].rank(method='dense', ascending=False).astype(int)
        
        # Sort legend by final rank (most recent year)
        if len(df_lang_rank_comp) > 0:
            final_ranks = df_lang_rank_comp[df_lang_rank_comp['year'] == df_lang_rank_comp['year'].max()].set_index('language')['rank']
            category_order = final_ranks.sort_values().index.tolist()
        else:
            category_order = None
        
        fig_lang_comp = px.line(
            df_lang_rank_comp,
            x='year',
            y='rank',
            color='language',
            markers=True,
            title=f'Programming Languages (Rank by {metric_type.capitalize()})',
            labels={'rank': 'Rank', 'year': 'Year', 'language': 'Language'},
            color_discrete_sequence=px.colors.qualitative.Set3,
            category_orders={'language': category_order} if category_order else None
        )
        fig_lang_comp.update_layout(
            height=500, 
            showlegend=True,
            yaxis={
                'autorange': 'reversed',  # Rank 1 at top
                'tickmode': 'linear',
                'tick0': 1,
                'dtick': 1,
                'title': 'Rank (1 = Best)'
            },
            hovermode='x unified',
            template='presentation',
           
        )
#         fig_lang_comp.update_layout(
#             xaxis_title=dict(font=dict(size=22)),
#             yaxis_title=dict(font=dict(size=22))
#         )
#         fig_lang_comp.update_yaxes(tickfont=dict(size=20))
#         fig_lang_comp.update_xaxes(tickfont=dict(size=20))
#         fig_lang_comp.update_layout(
#             legend=dict(
#                 #font=dict(size=22),
#                 orientation="h",  # Horizontal orientation
#                 yanchor="bottom", # Anchor the legend's bottom to the y position
#                 #y=-0.3,           # Position below the plot (0 is the bottom of the plot area, negative values move it outside)
#                 xanchor="left",   # Anchor the legend's left to the x position
#                 #x=0  
#                         ),
#              title_font_size=28, # Directly set the title font size

#         )
        
        st.plotly_chart(fig_lang_comp, use_container_width=True)

    with col2:
        # Topics percentage chart
        df_topics_rank_comp = df_topics_filtered.groupby(['year', 'topic'])[metric_type].sum().reset_index()
        
        # Get top 10 topics by total stars/forks
        top_topics = df_topics_rank_comp.groupby('topic')[metric_type].sum().nlargest(10).index
        df_topics_rank_comp = df_topics_rank_comp[df_topics_rank_comp['topic'].isin(top_topics)]
        
        # Calculate rank for each year - rank 1 = highest stars/forks
        df_topics_rank_comp['rank'] = df_topics_rank_comp.groupby('year')[metric_type].rank(method='dense', ascending=False).astype(int)
        
        # Sort legend by final rank (most recent year)
        if len(df_topics_rank_comp) > 0:
            final_ranks_topics = df_topics_rank_comp[df_topics_rank_comp['year'] == df_topics_rank_comp['year'].max()].set_index('topic')['rank']
            category_order_topics = final_ranks_topics.sort_values().index.tolist()
        else:
            category_order_topics = None
        
        fig_topics_comp = px.line(
            df_topics_rank_comp,
            x='year',
            y='rank',
            color='topic',
            markers=True,
            title=f'Top 10 Topics (Rank by {metric_type.capitalize()})',
            labels={'rank': 'Rank', 'year': 'Year', 'topic': 'Topic'},
            color_discrete_sequence=px.colors.qualitative.Pastel,
            category_orders={'topic': category_order_topics} if category_order_topics else None
        )
        fig_topics_comp.update_layout(
            height=500, 
            showlegend=True,
            yaxis={
                'autorange': 'reversed',  # Rank 1 at top
                'tickmode': 'linear',
                'tick0': 1,
                'dtick': 1,
                'title': 'Rank (1 = Best)'
            },
            hovermode='x unified',
            template='presentation'
        )
        st.plotly_chart(fig_topics_comp, use_container_width=True)

    with st.expander("Programming Languages and Topic Trends (Percentage)"):
        
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
            
    with st.expander("Raw and Cumulative Count of Stars/Forks for Programming Languages"):    
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

    st.markdown("---")

    # Race Chart Visualizations
    st.subheader("🏆 Race Chart Visualizations")

    col_race1, col_race2 = st.columns(2)

    with col_race1:
        st.markdown("##### Programming Languages Race Chart")

        mp4_url_programming_language_x_bioinformatics = "https://github.com/jpsglouzon/bio-lang-race/blob/main/figure/programming_language_x_bioinformatics.mp4?raw=true"
        st.video(mp4_url_programming_language_x_bioinformatics, format="video/mp4")

    with col_race2:
        st.markdown("##### Topics Race Chart")

        mp4_url_topics_x_bioinformatics = "https://github.com/jpsglouzon/bio-lang-race/blob/main/figure/topics_x_bioinformatics.mp4?raw=true"
        st.video(mp4_url_topics_x_bioinformatics, format="video/mp4")
    st.markdown("---")


        
    with st.expander("Full Race Charts"):    
            # 2 & 3. Raw count and Cumulative count side by side
            col_race1, col_race2 = st.columns(2)

    with col_race1:
        st.markdown("##### Programming Languages Race Chart")

        mp4_url_programming_language_x_bioinformatics_full = "https://github.com/jpsglouzon/bio-lang-race/blob/main/figure/programming_language_x_bioinformatics_full.mp4?raw=true"
        st.video(mp4_url_programming_language_x_bioinformatics_full, format="video/mp4")

    with col_race2:
        st.markdown("##### Topics Race Chart")

        mp4_url_topics_x_bioinformatics = "https://github.com/jpsglouzon/bio-lang-race/blob/main/figure/topics_x_bioinformatics_20.mp4?raw=true"
        st.video(mp4_url_topics_x_bioinformatics, format="video/mp4")
    st.markdown("---")
            
# TAB 2: TOPICS & RACE COMPARISONS (MERGED)
with tab2:
    st.header("🌟 Top 20 Repositories")

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
    fig_top_repos.update_traces(width=0.5) 

    fig_top_repos.update_layout(
        height=700,
        yaxis={'categoryorder': 'total ascending'},
        
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
