import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, Markdown

PROJECT_ROOT = Path.cwd().resolve().parents[0]
PROCESSED_DATA_DIR = PROJECT_ROOT / 'data' / 'processed'
OUTPUT_DIR = PROJECT_ROOT / 'figures' / 'pubmed_exploratory'

def process_author_data(cell_authors, nature_authors):
    cell_authors['publication'] = 'Cell'
    nature_authors['publication'] = 'Nature'
    cell_authors = cell_authors.set_index('PMID')
    nature_authors = nature_authors.set_index('PMID')

    cell_authors['primary_country'] = cell_authors['primary_country'].replace('No affiliation', np.nan)
    cell_authors['primary_country'] = cell_authors['primary_country'].fillna(
        cell_authors.groupby('PMID')['primary_country'].transform('first'))

    nature_authors['primary_country'] = nature_authors['primary_country'].replace('No affiliation', np.nan)
    nature_authors['primary_country'] = nature_authors['primary_country'].fillna(
        nature_authors.groupby('PMID')['primary_country'].transform('first'))

    all_authors = pd.concat([cell_authors, nature_authors])

    return all_authors

def pubmed_fig_1(all_authors):
    plot_df = all_authors.reset_index().groupby(['year', 'publication'])['PMID'].nunique().reset_index()
    plt.figure(figsize=(10,6))
    sns.lineplot(data = plot_df, x = 'year', y = 'PMID', hue = 'publication',
                linewidth = 2.5)
    plt.title('Fig. 1: publications per year, 2000-2026', fontsize = 18)
    plt.ylabel('number of publications', fontsize = 14)
    plt.xlabel('year', fontsize = 14)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.yticks(fontsize = 11)
    plt.xticks(plot_df['year'].unique(), rotation=45, fontsize = 11)
    plt.legend(frameon=False, fontsize = 14)
    sns.despine()
    plt.savefig(OUTPUT_DIR / 'fig_1_publications_per_year.png',
                dpi = 300,
                bbox_inches = 'tight',
                transparent = True)
    plt.show()
    comment = ("#### Figure 1 takeaways: publication number holds steady over time for each journal.")
    display(Markdown(comment))

def pubmed_fig_2(all_authors):
    plot_df = all_authors.reset_index().groupby(['year', 'publication']).size().reset_index(name='num_authors')
    plt.figure(figsize=(10,6))
    sns.lineplot(data = plot_df, x = 'year', y = 'num_authors', hue = 'publication',
                linewidth = 2.5)
    plt.title('Fig. 2: authors per year, 2000-2026', fontsize = 18)
    plt.ylabel('number of authors', fontsize = 14)
    plt.xlabel('year', fontsize = 14)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.yticks(fontsize = 11)
    plt.xticks(plot_df['year'].unique(), rotation=45, fontsize = 11)
    plt.legend(frameon=False, fontsize = 14)
    sns.despine()
    plt.savefig(OUTPUT_DIR / 'fig_2_authors_per_year.png',
                dpi = 300,
                bbox_inches = 'tight',
                transparent = True)
    plt.show()
    comment = ("#### Figure 2 takeaways: total number of authors increase over time.")
    display(Markdown(comment))

def pubmed_fig_3(all_authors):
    plot_df = all_authors.reset_index().groupby(['year', 'publication', 'PMID']).size().reset_index(name='authors_per_paper')
    plt.figure(figsize=(10,6))
    sns.lineplot(data = plot_df, x = 'year', y = 'authors_per_paper', hue = 'publication',
                linewidth = 2.5,
                estimator = 'mean')
    plt.title('Fig. 3: average authors per publication, 2000-2026', fontsize = 18)
    plt.ylabel('number of authors per publication', fontsize = 14)
    plt.xlabel('year', fontsize = 14)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.yticks(fontsize = 11)
    plt.xticks(plot_df['year'].unique(), rotation=45, fontsize = 11)
    plt.legend(frameon=False, fontsize = 14)
    sns.despine()
    plt.savefig(OUTPUT_DIR / 'fig_3_avg_authors_per_publication.png',
                dpi = 300,
                bbox_inches = 'tight',
                transparent = True)
    
    plt.show()
    comment = ("#### Figure 3 takeaways: average number of authors per publication also increases over time.")
    display(Markdown(comment))
    
def pubmed_fig_4(all_authors):
    plot_df = all_authors.reset_index().groupby(['year', 'publication', 'PMID'])['primary_country'].nunique().reset_index(name='countries_per_paper')
    plt.figure(figsize=(10,6))
    sns.lineplot(data = plot_df, x = 'year', y = 'countries_per_paper', hue = 'publication',
                linewidth = 2.5,
                estimator = 'mean')
    plt.title('Fig. 4: average number of countries per publication, 2000-2026', fontsize = 18)
    plt.ylabel('number of countries per publication', fontsize = 14)
    plt.xlabel('year', fontsize = 14)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.yticks(fontsize = 11)
    plt.xticks(plot_df['year'].unique(), rotation=45, fontsize = 11)
    plt.legend(frameon=False, fontsize = 14)
    sns.despine()
    plt.savefig(OUTPUT_DIR / 'fig_4_avg_countries_per_publication.png',
                dpi = 300,
                bbox_inches = 'tight',
                transparent = True)
    plt.show()
    comment = ("#### Figure 4 takeaways: number of countries involved in each publication also tends to increase over time "
               "Note: pre-2014 authorship affiliation (and therefore country) was not consistently recorded. "
               "Subsequent analyses done with data post-2014.")
    display(Markdown(comment))

def create_cooccur_and_crosstab(all_authors):
    # since affiliations were not fully recored before 2014, restrict
    # rest of analysis to post 2014 data. Also restrict to countries that
    # appear more than 25 times
    filtered = all_authors[all_authors['year'] >= 2014].dropna()
    filtered = filtered[filtered['primary_country'].map(filtered['primary_country'].value_counts() > 25)]

    #get the top 5 highest authorship countries
    top_5 = list(filtered['primary_country'].value_counts().iloc[0:5].index)

    # drop duplicates to ensure only counting a country once per PMID 
    # (e.g., if a paper has 3 USA authors, we only want USA listed once for that paper)
    df_unique = filtered.reset_index().drop_duplicates(subset=['PMID', 'primary_country'])

    # merge the dataframe with itself on PMID to create all country pairs
    pairs = df_unique.merge(df_unique, on='PMID', suffixes=('_target', '_partner'))

    # filter out self-matches (don't want to count USA pairing with USA)
    pairs = pairs[pairs['primary_country_target'] != pairs['primary_country_partner']]

    # group by the two country columns and count the occurrences
    co_occurrences = pairs.groupby(['primary_country_target', 'primary_country_partner']).size().reset_index(name='Count')

    # sort the results so the highest counts appear first
    co_occurrences = co_occurrences.sort_values(by=['primary_country_target', 'Count'], ascending=[True, False])
    # save co-occurences
    co_occurrences.to_csv(PROCESSED_DATA_DIR / 'country_co-occurences.csv')

    # create crosstabs
    # groupby PMID and count countries to get unique countries per paper
    df_unique['total_countries'] = df_unique.groupby('PMID')['primary_country'].transform('count')

    # for each row, subtract 1 to get the number of countries aside from
    # that country that contributed to the paper
    df_unique['other_countries'] = df_unique['total_countries'] - 1

    # for each primary country, compute crosstab to get frequency of collaborations
    # with other countries
    collaboration_counts = pd.crosstab(
        index=df_unique['primary_country'], 
        columns=df_unique['other_countries']
    )

    # sum up values over 15 to get an aggregate value for papers with over
    # 15 collaborating countries
    cond = collaboration_counts.columns[collaboration_counts.columns > 15]
    collaboration_counts['>15'] = collaboration_counts[cond].sum(axis=1)
    collaboration_counts = collaboration_counts.drop(columns = cond)

    # normalize the collab counts by the sum of papers
    norm_collab_counts = collaboration_counts.div(collaboration_counts.sum(axis=1),axis=0)

    # save to csvs
    collaboration_counts.to_csv(PROCESSED_DATA_DIR / 'collab_counts.csv')
    norm_collab_counts.to_csv(PROCESSED_DATA_DIR / 'norm_collab_counts.csv')

    return collaboration_counts, norm_collab_counts, co_occurrences, top_5, filtered

def pubmed_fig_5(norm_collab_counts, top_5):
    # transform normalized counts to long format for plotting
    long_counts = norm_collab_counts.reset_index().melt(
        id_vars = 'primary_country',
        var_name = 'num_collab_countries',
        value_name = 'proportion'
    )
    # change value to str for plotting appropriately
    long_counts['num_collab_countries'] = long_counts['num_collab_countries'].astype(str)
    cond = long_counts['primary_country'].isin(top_5)

    country_colors = {
        'USA': '#1f77b4',     # Hex code for a nice blue
        'Germany': '#ff7f0e',  # Orange
        'China': '#d62728',   # Red
        'France': '#2ca02c',   # Green
        'UK': '#9467bd', # Purple
    }

    plt.figure(figsize=(10,6))
    ax = sns.lineplot(
        data = long_counts[cond],
        x = 'num_collab_countries',
        y = 'proportion',
        hue = 'primary_country',
        linewidth = 2.5,
        alpha = 0.8,
        palette= country_colors
    )
    plt.title('Fig. 5: proportion of collaborating countries on publications from top 5 nations', fontsize = 18)
    plt.ylabel('proportion of publications', fontsize = 14)
    plt.xlabel('number of collaborating countries', fontsize = 14)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.yticks(fontsize = 11)
    plt.xticks(rotation=0, fontsize = 11)
    plt.legend(frameon=False, fontsize = 14)
    sns.despine()
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    plt.savefig(OUTPUT_DIR / 'fig_5_proportion_collab_countries_top_5.png',
                dpi = 300,
                bbox_inches = 'tight',
                transparent = True)
    plt.show()
    comment = ("#### Figure 5 takeaways: USA and China have the highest proportion of publications with authors from only that country. "
               "Other countries tend to have less solo-country publications. Solo-country publications are generally a minority.")
    display(Markdown(comment))
    
def pubmed_fig_6(filtered):
    plot_data = filtered.reset_index().drop_duplicates(subset=['PMID','primary_country'])
    plot_series = plot_data['primary_country'].value_counts()[0:20]
    plt.figure(figsize=(10,6))
    sns.barplot(data=plot_series, color = '#457b9d')
    plt.title('Top 20 countries by total number of publications, 2014-2026', fontsize = 18)
    plt.ylabel('number of publications', fontsize = 14)
    plt.xlabel('')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.yticks(fontsize = 11)
    plt.xticks(plot_series.index.unique(), rotation=90, fontsize = 11)
    sns.despine()
    plt.savefig(OUTPUT_DIR / 'fig_6_top_20_by_total_publications.png',
                dpi = 300,
                bbox_inches = 'tight',
                transparent = True)
    plt.show()
    comment = ("#### Figure 6 takeaways: summing the number of publications each country has appeared on shows the USA "
               "has by far the most affiliated papers for this time period, with the UK, Germany, and China following.")
    display(Markdown(comment))
    
def pubmed_fig_7(co_occurences):
    plot_series = co_occurences.groupby('primary_country_target')['Count'].sum().sort_values(ascending=False)[0:20]
    plt.figure(figsize=(10,6))
    sns.barplot(data=plot_series, color = '#457b9d')
    plt.title('Fig. 7: top 20 countries by total number of collaborations, 2014-2026', fontsize = 18)
    plt.ylabel('number of collaborations', fontsize = 14)
    plt.xlabel('')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.yticks(fontsize = 11)
    plt.xticks(plot_series.index.unique(), rotation=90, fontsize = 11)
    sns.despine()
    plt.savefig(OUTPUT_DIR / 'fig_7_top_20_by_total_collaborations.png',
                dpi = 300,
                bbox_inches = 'tight',
                transparent = True)
    plt.show()
    comment = ("#### Figure 7 details: Collaborations were calculated by summing the number of times each country appears with another "
               "country on a paper. For instance, if the USA appears with Japan on publication 1, and with Japan and the UK on publication 2, "
               "that would count as three collaborations for the USA (Japan + Japan + UK), three for Japan (USA + USA + UK), "
               "and two for UK (Japan + USA). Even if a multiple authors appear from a single country on a paper, that is counted "
               "as one instance of that country for the paper. "
               "\n#### Takeaways: certain countries like the UK and Germany have high number of collaborations relative to publication count.")
    display(Markdown(comment))
    
def run():
    cell_authors = pd.read_csv(PROCESSED_DATA_DIR / 'cell_processed_author_data.csv')
    nature_authors = pd.read_csv(PROCESSED_DATA_DIR / 'nature_processed_author_data.csv')
    all_authors = process_author_data(cell_authors, nature_authors)
    pubmed_fig_1(all_authors)
    pubmed_fig_2(all_authors)
    pubmed_fig_3(all_authors)
    pubmed_fig_4(all_authors)
    collaboration_counts, norm_collab_counts, co_occurrences, top_5, filtered = create_cooccur_and_crosstab(all_authors)
    pubmed_fig_5(norm_collab_counts, top_5)
    pubmed_fig_6(filtered)
    pubmed_fig_7(co_occurrences)