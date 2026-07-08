import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, Markdown

ROOT_PATH = Path.cwd().resolve().parents[0]
DATA_PATH = ROOT_PATH / 'data' / 'processed'
OUTPUT_DIR = ROOT_PATH / 'figures' / 'unesco_exploratory'

def process_unesco_data(inbound, outbound):
    # drop unneeded column and years after 2024 as there are few values
    # also drop rows with nan country
    inbound = inbound[inbound['year'] < 2024].drop(columns=['Unnamed: 0']).dropna(subset = ['country'])
    outbound = outbound[outbound['year'] < 2024].drop(columns=['Unnamed: 0']).dropna(subset=['country'])

    inbound = inbound.rename(columns = {'value': 'students'})
    outbound = outbound.rename(columns = {'value': 'students'})

    # merge inbound and outbound and calculate student flux
    merged = inbound.merge(outbound, on=['country', 'year'], suffixes = ('_inbound', '_outbound')).drop(columns = ['geoUnit_outbound'])
    merged['flux'] = merged['students_inbound'].sub(merged['students_outbound'])
    merged['total_exchange'] = merged['students_inbound'].add(merged['students_outbound'])
    merged.to_csv(DATA_PATH / 'merged_student_data.csv')

    return inbound, outbound, merged

def unesco_fig_8(inbound):
    top_6_inbound = list(inbound.groupby('country')['students'].sum().sort_values(ascending=False)[0:6].index)
    plt.figure(figsize=(10,6))
    cond = inbound['country'].isin(top_6_inbound)
    country_colors = {
        'USA': '#1f77b4',     # Blue
        'Australia': '#ff7f0e',  # Orange
        'Canada': '#d62728',   # Red
        'France': '#2ca02c',   # Green
        'UK': '#9467bd', # Purple
        'Russia': '#333333'
    }
    sns.lineplot(data = inbound[cond], x = 'year', y = 'students', hue = 'country',
                linewidth = 2.5,
                palette=country_colors)
    plt.title('Fig. 8: number of inbound tertiary students, top 6 countries', fontsize = 18)
    plt.ylabel('number of students (millions)', fontsize = 14)
    plt.xlabel('year', fontsize = 14)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.yticks(fontsize = 11)
    plt.xticks(inbound['year'].unique(), rotation=45, fontsize = 11)
    plt.legend(frameon=False, fontsize = 14)
    sns.despine()
    plt.savefig(OUTPUT_DIR / 'fig_8_num_inbound_students_top_6.png',
                dpi = 300,
                bbox_inches = 'tight',
                transparent = True)
    plt.show()
    comment = ("#### Figure 8 takeaways: for the top 6 countries by total inbound students, the number of inbound students has "
        "generally increased over time.")
    display(Markdown(comment))
    
def unesco_fig_9(outbound):
    top_6_outbound = list(outbound.groupby('country')['students'].sum().sort_values(ascending=False)[0:6].index)
    plt.figure(figsize=(10,6))
    cond = outbound['country'].isin(top_6_outbound)
    country_colors = {
        'USA': '#1f77b4',     # Hex code for a nice blue
        'Germany': '#ff7f0e',  # Orange
        'China': '#d62728',   # Red
        'France': '#2ca02c',   # Green
        'India': '#9467bd', # Purple
        'Korea': '#333333'
    }
    sns.lineplot(data = outbound[cond], x = 'year', y = 'students', hue = 'country',
                linewidth = 2.5,
                palette=country_colors)
    plt.title('Fig. 9: number of outbound tertiary students, top 6 countries', fontsize = 18)
    plt.ylabel('number of students (millions)', fontsize = 14)
    plt.xlabel('year', fontsize = 14)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.yticks(fontsize = 11)
    plt.xticks(outbound['year'].unique(), rotation=45, fontsize = 11)
    plt.legend(frameon=False, fontsize = 14)
    sns.despine()
    plt.savefig(OUTPUT_DIR / 'fig_9_num_outbound_students_top_6.png',
                dpi = 300,
                bbox_inches = 'tight',
                transparent = True)
    plt.show()
    comment = ("#### Figure 9 takeaways: China and India have the highest number of outbound students, with numbers"
                " rising over time.")
    display(Markdown(comment))
    
def unesco_fig_10(merged):
    top_10 = merged.groupby('country')['flux'].sum().sort_values(ascending=False)[0:10]
    bottom_10 = merged.groupby('country')['flux'].sum().sort_values(ascending=True)[0:10]
    plot_series = pd.concat([top_10, bottom_10.sort_values(ascending=False)], axis=0)
    plt.figure(figsize=(10,6))
    sns.barplot(data=plot_series, color = '#457b9d')
    plt.title('Fig. 10: total student flux 2000-2023, top and bottom 10 countries', fontsize = 18)
    plt.ylabel('number of students (tens of millions)', fontsize = 14)
    plt.xlabel('')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.yticks(fontsize = 11)
    plt.xticks(plot_series.index.unique(), rotation=90, fontsize = 11)
    sns.despine()
    plt.savefig(OUTPUT_DIR / 'fig_10_total_student_flux_top_bottom_10.png',
                dpi = 300,
                bbox_inches = 'tight',
                transparent = True)
    plt.show()
    comment = ("#### Figure 10 takeaways: student flux is calculated as (inbound students - outbound students). Anglosphere "
         "countries have the highest inbound flux over the time period. Japan is also in the top 10 for inbound.")
    display(Markdown(comment))
    
def unesco_fig_11(merged):
    top_20_total_exchange = merged.groupby('country')['total_exchange'].sum().sort_values(ascending=False)[0:20]
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(data=merged[merged['country'].isin(list(top_20_total_exchange.index))].groupby('country')['total_exchange'].sum().sort_values(),
                color = '#e76f51')
    order = list(merged[merged['country'].isin(list(top_20_total_exchange.index))].groupby('country')['total_exchange'].sum().sort_values().index)
    sns.barplot(data=merged[merged['country'].isin(list(top_20_total_exchange.index))].groupby('country')['students_inbound'].sum(),
                order = order,
                color = '#2a9d8f')
    plt.title('Fig. 11: total student exchange (inbound + outbound), top 20 countries', fontsize = 18)
    plt.ylabel('number of students (tens of millions)', fontsize = 14)
    plt.xlabel('')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.yticks(fontsize = 11)
    plt.xticks(rotation=90, fontsize = 11)
    sns.despine()

    legend_data = [
        {"color": "#e76f51", "label": "outbound students"},
        {"color": "#2a9d8f", "label": "inbound students"}
    ]
    start_x = 0.1
    start_y = 0.85
    line_spacing = 0.08  # How much to drop down for each legend item

    for i, item in enumerate(legend_data):
        current_y = start_y - (i * line_spacing)
        
        # Draw the solid colored square (Using the \u25A0 unicode character)
        ax.text(
            x=start_x, 
            y=current_y, 
            s="■", 
            color=item["color"], 
            fontsize=16,          
            va="center", 
            ha="left",
            transform=ax.transAxes # Uses 0-1 coordinate system relative to the chart axes
        )
        
        # Draw the text label right next to it
        ax.text(
            x=start_x + 0.04,     # Shift the text slightly to the right of the square
            y=current_y - 0.005, 
            s=item["label"], 
            color="#000000",       
            fontsize=12,
            va="center", 
            ha="left",
            transform=ax.transAxes
        )

    plt.savefig(OUTPUT_DIR / 'fig_11_total_student_exchange_top_20.png',
                dpi = 300,
                bbox_inches = 'tight',
                transparent = True)
    plt.show()
    comment = ("#### Figure 11 takeaways: plotting inbound and outbound students on top of one another reveals proportionality "
               "of inbound and outbound students in countries with the top 20 total student exchanges.")
    display(Markdown(comment))

def run():
    inbound = pd.read_csv(DATA_PATH / 'inbound_students_processed.csv')
    outbound = pd.read_csv(DATA_PATH / 'outbound_students_processed.csv')
    inbound, outbound, merged = process_unesco_data(inbound, outbound)

    unesco_fig_8(inbound)
    unesco_fig_9(outbound)
    unesco_fig_10(merged)
    unesco_fig_11(merged)
