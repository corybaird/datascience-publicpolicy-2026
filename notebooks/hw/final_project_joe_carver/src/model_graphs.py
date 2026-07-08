import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, Markdown
from scipy import stats

PROJECT_ROOT = Path.cwd().resolve().parents[0]
PROCESSED_DATA_DIR = PROJECT_ROOT / 'data' / 'processed'
OUTPUT_DIR = PROJECT_ROOT / 'figures' / 'model'

def preprocess():
    #pre-process data slightly to get grouped metrics
    merged_students = pd.read_csv(PROCESSED_DATA_DIR / 'merged_student_data.csv', index_col=0)
    total_inbound = merged_students.groupby('country')['students_inbound'].sum()
    total_outbound = merged_students.groupby('country')['students_outbound'].sum()
    total_exchange = merged_students.groupby('country')['total_exchange'].sum()

    collab_counts = pd.read_csv(PROCESSED_DATA_DIR / 'collab_counts.csv', index_col = 0)
    collab_counts['total_collabs'] = collab_counts[['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','>15']].sum(axis=1)
    collab_counts['solo_collab_ratio'] = collab_counts['0'].div(collab_counts['total_collabs'] + collab_counts['0'])
    collab_counts['total_publications'] = collab_counts[['0', 'total_collabs']].sum(axis=1)

    #join unesco student data and collaboration/publication data
    unesco_pubmed = collab_counts.join([total_exchange, total_inbound, total_outbound], how = 'inner')
    unesco_pubmed['collab_ratio'] = unesco_pubmed['total_collabs'] / (unesco_pubmed['total_collabs'] + unesco_pubmed['0'])



    #create an ignore list with three countries that are relative outliers in the data
    # ignore_list = ['USA', 'China', 'India']
    # unesco_pubmed = unesco_pubmed.drop(ignore_list)

    #create lists of the x and y variables of interest
    x_vars = ['students_inbound', 'students_outbound', 'total_exchange']
    y_vars = ['total_publications', 'total_collabs', 'collab_ratio']

    # get logs of the variables of interest 
    for var in x_vars:
        unesco_pubmed[f'log_{var}'] = np.log(unesco_pubmed[var])
    for var in y_vars:
        unesco_pubmed[f'log_{var}'] = np.log(unesco_pubmed[var])

    # create list of log variables
    logx_vars = ['log_students_inbound', 'log_students_outbound', 'log_total_exchange']
    logy_vars = ['log_total_publications', 'log_total_collabs', 'log_collab_ratio']

    return unesco_pubmed, logx_vars, logy_vars, y_vars

def run():
    unesco_pubmed, logx_vars, logy_vars, y_vars = preprocess()
    model_fig_12(unesco_pubmed, logx_vars, logy_vars)
    model_fig_13(unesco_pubmed, logx_vars, logy_vars)
    model_fig_14(unesco_pubmed, logx_vars, y_vars)

#use stats from scipy to return linear regression results
def get_lin_regress(df, x_var, y_var, x_log = False):
    slope, intercept, r_value, p_value, std_err = stats.linregress(
    np.log(df[x_var]) if x_log else df[x_var],
    df[y_var]
    )
    return slope, intercept, r_value, p_value, std_err

# define countries to highlight in the plots
highlight_countries = ['China', 'India', 'USA', 'Japan', 'UK', 'Australia', 'Russia']

#plot linear regression with confidence intervals using seaborn.regplot
def plot_lin_regress(df, x_var, y_var,ax, log_x=False):
    return sns.regplot(data = df, x = x_var, y = y_var, ax=ax, logx=log_x,
        scatter_kws={
        'color': '#457b9d',
        'alpha': 0.6,       
        's': 20,           
        'edgecolor': 'black'
        },
        line_kws={
        'color': '#e63946', 
        'alpha': 1.0,     
        'linewidth': 2 
    })

def model_fig_12(unesco_pubmed, logx_vars, logy_vars):
    unesco_pubmed, logx_vars, logy_vars = unesco_pubmed, logx_vars, logy_vars
    fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (10,4))
    axes = axes.flatten()
    y_var = logy_vars[0]
    highlights = unesco_pubmed.loc[highlight_countries]
    for i, x_var in enumerate(logx_vars):
            ax = axes[i]
            slope, intercept, r_value, p_value, std_err = get_lin_regress(unesco_pubmed, x_var, y_var)
            plot_lin_regress(unesco_pubmed, x_var, y_var, ax)
            ax.set_xlabel(x_var.replace('_', ' '))
            ax.set_ylabel(y_var.replace('_', ' ').replace('collabs', 'collaborations').replace('collab', 'collaboration'))
            
            # regression r-squared and p-value text
            ax.text(
            x=0.05, 
            y=1.075, 
            s=f'fit R\u00B2: {r_value**2:.2f}, p-value: {p_value:.1e}', 
            transform=ax.transAxes, 
            verticalalignment='top',
            fontsize=10
            )
            # separate scatter for highlight countries
            sns.scatterplot(
            data=highlights, 
            x=x_var, 
            y=y_var, 
            ax=ax, 
            color='#e63946',
            edgecolor='black',
            s=40,           
            zorder=5        
            )
            for index, row in highlights.iterrows():
                ax.text(
                x=row[x_var] + unesco_pubmed[x_var].max()/50, # Add a small offset so text doesn't hit the dot
                y=row[y_var] - unesco_pubmed[y_var].max()/50, 
                s=index,                  
                fontdict={'color': '#000000', 'size': 8},
                verticalalignment='center',
                bbox=dict(facecolor='white', edgecolor='lightgrey', boxstyle='round,pad=0.2', alpha=0.8),
                zorder = 30
                )
            sns.despine()

    fig.suptitle('Fig. 12: student metrics vs. total publications - log-log regression analysis')        
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig_12_student_metrics_vs_total_pubs.png',
                    dpi = 300,
                    bbox_inches = 'tight',
                    transparent = True)
    plt.show()
    comment = ("#### Figure 12 takeaways: there is decent correlation between total inbound students and total student exchange and publication counts "
                "with weaker correlation with outbound students.")
    display(Markdown(comment))

def model_fig_13(unesco_pubmed, logx_vars, logy_vars):
    unesco_pubmed, logx_vars, logy_vars = unesco_pubmed, logx_vars, logy_vars
    fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (10,4))
    axes = axes.flatten()
    y_var = logy_vars[1]
    highlights = unesco_pubmed.loc[highlight_countries]
    for i, x_var in enumerate(logx_vars):
            ax = axes[i]
            slope, intercept, r_value, p_value, std_err = get_lin_regress(unesco_pubmed, x_var, y_var)
            plot_lin_regress(unesco_pubmed, x_var, y_var, ax)
            ax.set_xlabel(x_var.replace('_', ' '))
            ax.set_ylabel(y_var.replace('_', ' ').replace('collab', 'collaboration'))
            
            # regression r-squared and p-value text
            ax.text(
            x=0.05, 
            y=1.075, 
            s=f'fit R\u00B2: {r_value**2:.2f}, p-value: {p_value:.1e}', 
            transform=ax.transAxes, 
            verticalalignment='top',
            fontsize=10
            )
            # separate scatter for highlight countries
            sns.scatterplot(
            data=highlights, 
            x=x_var, 
            y=y_var, 
            ax=ax, 
            color='#e63946',
            edgecolor='black',
            s=40,           
            zorder=5        
            )
            for index, row in highlights.iterrows():
                ax.text(
                x=row[x_var] + unesco_pubmed[x_var].max()/50, # Add a small offset so text doesn't hit the dot
                y=row[y_var] - unesco_pubmed[y_var].max()/50, 
                s=index,                  
                fontdict={'color': '#000000', 'size': 8},
                verticalalignment='center',
                bbox=dict(facecolor='white', edgecolor='lightgrey', boxstyle='round,pad=0.2', alpha=0.8),
                zorder = 30
                )
            sns.despine()

    fig.suptitle('Fig. 13: student metrics vs. total collaborations - log-log regression analysis')        
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig_13_student_metrics_vs_total_collabs.png',
                    dpi = 300,
                    bbox_inches = 'tight',
                    transparent = True)
    plt.show()
    comment = ("#### Figure 13 takeaways: number of inbound students and total student exchange are moderately correlated with total collaborations. "
               "Outbound student numbers once again show less correlation.")
    display(Markdown(comment))

def model_fig_14(unesco_pubmed, logx_vars, logy_vars):
    unesco_pubmed, logx_vars, y_vars = unesco_pubmed, logx_vars, logy_vars
    fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (10,4))
    axes = axes.flatten()
    y_var = logy_vars[2]
    highlights = unesco_pubmed.loc[highlight_countries]
    for i, x_var in enumerate(logx_vars):
            ax = axes[i]
            slope, intercept, r_value, p_value, std_err = get_lin_regress(unesco_pubmed, x_var, y_var)
            plot_lin_regress(unesco_pubmed, x_var, y_var, ax)
            ax.set_xlabel(x_var.replace('_', ' '))
            ax.set_ylabel(y_var.replace('_', ' ').replace('collab', 'collaboration'))
            
            # regression r-squared and p-value text
            ax.text(
            x=0.05, 
            y=1.075, 
            s=f'fit R\u00B2: {r_value**2:.2f}, p-value: {p_value:.1e}', 
            transform=ax.transAxes, 
            verticalalignment='top',
            fontsize=10
            )
            # separate scatter for highlight countries
            sns.scatterplot(
            data=highlights, 
            x=x_var, 
            y=y_var, 
            ax=ax, 
            color='#e63946',
            edgecolor='black',
            s=40,           
            zorder=5        
            )
            for index, row in highlights.iterrows():
                ax.text(
                x=row[x_var] + unesco_pubmed[x_var].max()/50, # Add a small offset so text doesn't hit the dot
                y=row[y_var] - unesco_pubmed[y_var].max()/50, 
                s=index,                  
                fontdict={'color': '#000000', 'size': 8},
                verticalalignment='center',
                bbox=dict(facecolor='white', edgecolor='lightgrey', boxstyle='round,pad=0.2', alpha=0.8),
                zorder = 30
                )
            sns.despine()

    fig.suptitle('Fig. 14: student metrics vs. collaboration ratio - log-log regression analysis')        
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig_14_student_metrics_vs_collab_ratio.png',
                    dpi = 300,
                    bbox_inches = 'tight',
                    transparent = True)
    plt.show()
    comment = ("#### Figure 14 takeaways: the vast majority of countries have very high collaboration ratios (close to 1). "
               "There is little meaningful variation to fit the data on, although a trend towards higher student metrics and"
               "lower collaboration ratios (perhaps because less collaboration is needed with higher student population)")
    display(Markdown(comment))
    
