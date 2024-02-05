import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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

def generate_comparison_plots(data, team1, team2, selected_statistic):
    logger.info("Generating comparison plot for {} and {} for selected statistics: {}".format(team1, team2, selected_statistic))
    
    # Check if both team1 and team2 exist in the data
    if team1 not in data.index or team2 not in data.index:
        logger.error("One or both teams not found in the data.")
        return []

    # Create an empty list to store base64 strings for plots
    base64_strings = []
    logger.info("Selected Statistic: {}".format(selected_statistic))
    team1_stat = data.loc[team1, selected_statistic]
    team2_stat = data.loc[team2, selected_statistic]
    
    try:
        team1_stat = int(team1_stat[0].replace(',', ''))
        team2_stat = int(team2_stat[0].replace(',', ''))
    except:
        team1_stat = int(team1_stat[0])
        team2_stat = int(team2_stat[0])
    
    logger.info("Team 1 Stats: {} Type of: {}".format(team1_stat, type(team1_stat)))
    logger.info("Team 2 Stats: {} Type of: {}".format(team2_stat, type(team2_stat)))
    
    # Create the comparison plot for the single statistic
    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.35

    indices = np.arange(2)  # Two teams

    # Define colors for team1 and team2
    colors = ['blue', 'red']

    # Plot bars for team 1 and team 2 with assigned colors
    team_names = [str(team1), str(team2)]  # Convert to strings
    bars = ax.bar(indices - width/2, [team1_stat, team2_stat], width, tick_label=team_names, color=colors)
    ax.set_ylabel(selected_statistic)
    ax.set_title("{} for {} and {}".format(selected_statistic, team1, team2))

    # Add text annotations for the values at the top of each bar
    for bar, value in zip(bars, [team1_stat, team2_stat]):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 10, str(value), ha='center', va='bottom')

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    base64_strings.append(base64.b64encode(buf.read()).decode('utf-8'))

    return base64_strings

def generate_all_plots(data, statistics):
    # Number of teams
    num_teams = len(data.index)

    # Create a figure with subplots - one for each statistic
    num_statistics = len(statistics)
    fig, axes = plt.subplots(num_statistics, 1, figsize=(10, num_statistics * 5))

    # Generate a color map with unique colors for each team
    colors = plt.cm.hsv(np.linspace(0, 1, num_teams))

    for i, stat in enumerate(statistics):
        ax = axes[i] if num_statistics > 1 else axes
        values = data[stat].values
        team_names = data.index
        indices = np.arange(num_teams)

        values = [int(value.replace(',', '')) if isinstance(value, str) else int(value) for value in values]

        team_names, values = zip(*sorted(zip(team_names, values), key=lambda x: x[1], reverse=True))

        for j, value in enumerate(values):
            # Plot each bar individually and specify the color
            ax.bar(indices[j], value, color=colors[j], align='center', alpha=0.7)
            # Annotate the value on top of each bar
            ax.text(indices[j], value, str(value), ha='center', va='bottom')

        ax.set_xticks(indices)
        ax.set_xticklabels(team_names, rotation='vertical')
        ax.set_title(stat)

    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    base64_string = base64.b64encode(buf.read()).decode('utf-8')

    return [base64_string]

