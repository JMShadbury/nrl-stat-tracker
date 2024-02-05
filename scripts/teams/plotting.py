import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from util.logger import get_logger
import seaborn as sns  # Import seaborn for plotting

logger = get_logger()

def generate_plot(data, selected_team, statistic_name):
    # Ensure we are working with a DataFrame
    logger.info("Generating plot for {} - {}".format(selected_team, statistic_name))
    selected_statistic_data = data.loc[selected_team, statistic_name]
    
    # Customize the plotting logic for the specific statistic
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=selected_statistic_data.index, y=selected_statistic_data.values, ax=ax, palette='muted')
    ax.set_title(f'{statistic_name} for {selected_team}')
    ax.set_ylabel('Value')
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    base64_string = base64.b64encode(buf.read()).decode('utf-8')

    return base64_string


def generate_comparison_plots(data, team1, team2, selected_statistics):
    logger.info("Generating comparison plot for {} and {} for selected statistics: {}".format(team1, team2, selected_statistics))
    
    # Check if both team1 and team2 exist in the data
    if team1 not in data.index or team2 not in data.index:
        logger.error("One or both teams not found in the data.")
        return []

    # Check if all selected statistics exist in the data
    missing_statistics = [statistic for statistic in selected_statistics if statistic not in data.columns]
    if missing_statistics:
        logger.error("The following selected statistics do not exist in the data: {}".format(missing_statistics))
        return []
    
    # Filter the data to include only the selected statistics for team1 and team2
    team1_stats = data.loc[team1][selected_statistics].drop('TeamName', errors='ignore')
    team2_stats = data.loc[team2][selected_statistics].drop('TeamName', errors='ignore')
    logger.info("Team 1 Stats: {}".format(team1_stats))
    logger.info("Team 2 Stats: {}".format(team2_stats))

    # Create the comparison plot
    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.35  # width of the bars
    num_statistics = len(selected_statistics)  # This should be the actual count of statistics you're comparing

    indices = np.arange(num_statistics)
    for i, stat in enumerate(selected_statistics):
        # Calculate the offset to space the bars apart
        x_offset = (i - (num_statistics - 1) / 2) * width
        print(f"Plotting {stat}: index {indices}, x_offset {x_offset}, width {width}")
        # Plot bars for team 1 and team 2 with an offset
        ax.bar(indices - width/2 + x_offset, team1_stats[stat], width, label=team1)
        ax.bar(indices + width/2 + x_offset, team2_stats[stat], width, label=team2)
        print(f"Bar plotted for {stat}")

    ax.set_xticks(indices)
    ax.set_xticklabels(selected_statistics)

    ax.set_xticks(indices)
    ax.set_xticklabels(selected_statistics)
    ax.legend()

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    base64_string = base64.b64encode(buf.read()).decode('utf-8')

    return [base64_string]


