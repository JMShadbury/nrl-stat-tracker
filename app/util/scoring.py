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
    #PLAYED = -102.63299158823529
    TRIES = 1.74394
    LINE_ENGAGED = 0.16962499999999997
    COMPLETION = 0.4724
    SUPPORT = 0.1434
    LINE_BREAKS = 1.54813
    POST_CONTACT_METRES = 0.00896
    TACKLE_BREAKS = 0.22104
    RUN_METRES = 0.003861
    OFFLOADS = 0.5344
    KICK_METRES = 0.00816
    TRY_ASSISTS = 2.1667
    DECOY_RUNS = 0.15487499999999998
    DUMMY_HALF_RUNS = 0.4192
    MISSED_TACKLES = -0.1842
    CHARGE_DOWNS = 5
    INTERCEPTS = 7.7
    ERRORS = -0.4403
    INEFFECTIVE_TACKLES = -0.3286
    PENALTIES_CONCEDED = -0.8434
    HANDLING_ERRORS = -0.4762
    SHORT_DROPOUTS = -3.889
    FOURTY_TWENTY_KICKS = 5
    KICK_RETURN_METRES = 0.044005
    FIELD_GOALS = 5
    RUNS = 0.02381
    KICKS = 0.2318
    CONVERSION_PERCENTAGE = 0.0774



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
                logger.debug(f"NaN value encountered for statistic: {stat}")
                continue

            try:
                value_float = float(value_str)
                score += value_float * weight
            except ValueError:
                logger.debug(f"Could not convert value: {value} for statistic: {stat}")
        else:
            logger.debug(f"Ignoring unmapped statistic: {stat}")

    # Dynamic adjustment for PLAYED statistic
    played_nerf = set_games_played(team_stats)
    score += played_nerf

    if completion_rate > completion_rate_threshold:
        score += ScoringRules.COMPLETION_RATE.value * (completion_rate - completion_rate_threshold)
    logger.debug(f"Calculated score: {score}")
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
