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
    TRIES = 8
    GOALS = 3
    ALL_RECEIPTS = 0.0005
    LINE_ENGAGED = 0.005
    COMPLETION = 0.39
    SUPPORT = 0.95
    LINE_BREAKS = 5.88
    POST_CONTACT_METRES = 0.3
    TACKLE_BREAKS = 1.5
    RUN_METRES = 0.0005
    OFFLOADS = 4
    KICK_METRES = 0.018
    TRY_ASSISTS = 3.15
    DECOY_RUNS = 0.23
    DUMMY_HALF_RUNS = 1.24
    TACKLES = 0.03
    MISSED_TACKLES = -0.29
    CHARGE_DOWNS = 5
    INTERCEPTS = 5
    ERRORS = -0.95
    INEFFECTIVE_TACKLES = -0.64
    PENALTIES_CONCEDED = -1.79
    HANDLING_ERRORS = -1.14
    SHORT_DROPOUTS = -0.3
    FOURTY_TWENTY_KICKS = 0.6
    KICK_RETURN_METRES = 0.00005
    RUNS = 0.005
    KICKS = 0.02
    CONVERSION_PERCENTAGE = 0.015
    POSSESSION = 1
    
    
scoring_descriptions = {
    "TRIES": "Awarded for each try scored by the team.",
    "GOALS": "Awarded for each successful goal kicked by the team.",
    "ALL_RECEIPTS": "Awarded for each receipt of the ball by the team.",
    "LINE_ENGAGED": "Awarded for each time the team engages the line.",
    "COMPLETION": "Awarded for each time the team completes a set of six tackles.",
    "SUPPORT": "Awarded for each time the team supports a player with the ball.",
    "LINE_BREAKS": "Awarded for each line break made by the team.",
    "POST_CONTACT_METRES": "Awarded for each metre gained after contact with an opposing player.",
    "TACKLE_BREAKS": "Awarded for each tackle broken by the team.",
    "RUN_METRES": "Awarded for each metre gained by the team.",
    "OFFLOADS": "Awarded for each offload made by the team.",
    "KICK_METRES": "Awarded for each metre gained from a kick made by the team.",
    "TRY_ASSISTS": "Awarded for each try assist made by the team.",
    "DECOY_RUNS": "Awarded for each decoy run made by the team.",
    "DUMMY_HALF_RUNS": "Awarded for each dummy half run made by the team.",
    "TACKLES": "Awarded for each tackle made by the team.",
    "MISSED_TACKLES": "Deducted for each tackle missed by the team.",
    "CHARGE_DOWNS": "Awarded for each charge down made by the team.",
    "INTERCEPTS": "Awarded for each intercept made by the team.",
    "ERRORS": "Deducted for each error made by the team.",
    "INEFFECTIVE_TACKLES": "Deducted for each ineffective tackle made by the team.",
    "PENALTIES_CONCEDED": "Deducted for each penalty conceded by the team.",
    "HANDLING_ERRORS": "Deducted for each handling error made by the team.",
    "SHORT_DROPOUTS": "Deducted for each short dropout made by the team.",
    "FOURTY_TWENTY_KICKS": "Awarded for each 40/20 kick made by the team.",
    "KICK_RETURN_METRES": "Awarded for each metre gained from a kick return made by the team.",
    "RUNS": "Awarded for each run made by the team.",
    "KICKS": "Awarded for each kick made by the team.",
    "CONVERSION_PERCENTAGE": "Awarded for each percentage point of conversion rate achieved by the team.",
    "POSSESSION": "Awarded for each minute of possession held by the team."
}


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
