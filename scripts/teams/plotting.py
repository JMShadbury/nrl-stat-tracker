import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from util.logger import get_logger

logger = get_logger()

def generate_plot(data, selected_team):
    # Ensure we are working with a DataFram
    logger.info("Generating plot for {}".format(selected_team))
    selected_df = data.loc[selected_team].drop('TeamName', errors='ignore')
    logger.info("Selected Data: {}".format(selected_df))
    absolute_numbers = selected_df.drop('Conversion Percentage')  # Exclude percentages
    logger.info("Absolute Numbers: {}".format(absolute_numbers))
    
    logger.info("Creating plot for {}".format(selected_team))

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=absolute_numbers.index, y=absolute_numbers.values, ax=ax, palette='muted')
    ax.set_title(f'Statistics for {selected_team}')
    ax.set_ylabel('Value')

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    base64_string = base64.b64encode(buf.read()).decode('utf-8')
    
    logger.info("Plot data generated -: {}".format(base64_string))

    return base64_string

def generate_comparison_plots(data, team1, team2):
    # Example: Generate side-by-side bar plots for comparison
    # This is a simple example, and you might want to create more sophisticated comparisons
    logger.info("Generating comparison plot for {} And {}".format(team1, team2))
    team1_stats = data.loc[team1].drop('TeamName', errors='ignore')
    logger.info("Team 1 Stats: {}".format(team1_stats))
    team2_stats = data.loc[team2].drop('TeamName', errors='ignore')
    logger.info("Team 2 Stats: {}".format(team2_stats))
    
    logger.info("Creating comparison plot for {} And {}".format(team1, team2))

    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.35  # width of the bars

    indices = np.arange(len(team1_stats))
    ax.bar(indices - width/2, team1_stats, width, label=team1)
    ax.bar(indices + width/2, team2_stats, width, label=team2)

    ax.set_xticks(indices)
    ax.set_xticklabels(team1_stats.index)
    ax.legend()

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    base64_string = base64.b64encode(buf.read()).decode('utf-8')
    
    logger.info("Comparison plot data generated -: {}".format(base64_string))

    return [base64_string]
