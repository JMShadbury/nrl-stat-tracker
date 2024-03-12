"""
This module contains functionality for scoring and comparing teams 
based on various statistics.
"""

# pylint: disable=E0401
# pylint: disable=C0325
# pylint: disable=E1101
# pylint: disable=C0413
# pylint: disable=R1705

from enum import Enum
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from common.logger import get_logger



logger = get_logger()


class ScoringRules(Enum):
    """
    Enum for scoring rules.
    """
    TRIES = 0.5
    #PLAYED = -303.214
    LINE_ENGAGED = 0.05
    COMPLETION = 1
    SUPPORT = 0.5
    LINE_BREAKS = 0.6
    POST_CONTACT_METRES = 0.1
    TACKLE_BREAKS = 0.8
    RUN_METRES = 0.0002
    OFFLOADS = 2
    KICK_METRES = 0.002
    TRY_ASSISTS = 0.5
    DECOY_RUNS = 0.1
    DUMMY_HALF_RUNS = 0.5
    MISSED_TACKLES = -0.5
    CHARGE_DOWNS = 1
    INTERCEPTS = 1.5
    ERRORS = -0.5
    INEFFECTIVE_TACKLES = -0.05
    PENALTIES_CONCEDED = -0.05
    HANDLING_ERRORS = -0.05
    SHORT_DROPOUTS = -0.1
    FOURTY_TWENTY_KICKS = 3
    KICK_RETURN_METRES = 0.05
    TACKLES = 0.002
    FIELD_GOALS = 2
    RUNS = 0.001
    KICKS = 0.01
    CONVERSION_PERCENT = 0.2



def set_games_played(stats):
    """
    Calculate the nerfed games played statistic.
    """
    played = stats.get("PLAYED", 0)
    played_nerf = (played - played * 2)
    return played_nerf


def calculate_score(team_stats):
    """
    Calculate the score for a team based on their statistics.
    """
    score = 0
    completion_rate = team_stats.get("COMPLETION_RATE", 0)
    completion_rate_threshold = 70

    for stat, value in team_stats.items():
        if "40/20 Kicks" in stat:
            stat = "FOURTY_TWENTY_KICKS"
        formatted_stat = stat.replace(" ", "_").upper()

        if formatted_stat in ScoringRules.__members__:
            weight = ScoringRules[formatted_stat].value
            value_str = str(value).replace(",", "")

            if value_str == 'nan':
                logger.warning("NaN value encountered for statistic: %s", stat)
                continue

            try:
                value_float = float(value_str)
                score += value_float * weight
            except ValueError:
                logger.warning("Could not convert value: %s for statistic: %s", value, stat)
        else:
            logger.warning("Ignoring unmapped statistic: %s", stat)

    # Dynamic adjustment for PLAYED statistic
    played_nerf = set_games_played(team_stats)
    score += played_nerf

    if completion_rate > completion_rate_threshold:
        score += ScoringRules.COMPLETION_RATE.value * (completion_rate - completion_rate_threshold)
    logger.warning("Calculated score: %s", score)
    return score


def compare_teams(team_data, team1_name, team2_name):
    """
    Compare two teams and return the name of the team with the higher score.
    Returns "Tie" if scores are equal.
    """
    team1_data = team_data.loc[team1_name].to_dict()
    team2_data = team_data.loc[team2_name].to_dict()

    team1_score = calculate_score(team1_data)
    team2_score = calculate_score(team2_data)

    if team1_score > team2_score:
        return team1_name
    elif team2_score > team1_score:
        return team2_name
    else:
        return "Tie"
