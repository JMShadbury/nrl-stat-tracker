from util.logger import get_logger

logger = get_logger()

from enum import Enum

class ScoringRules(Enum):
    PLAYED = -9800
    LINE_ENGAGED = 3
    COMPLETION = 80
    SUPPORT = 3
    LINE_BREAKS = 20
    POST_CONTACT_METRES = 0.9
    TACKLE_BREAKS = 9
    RUN_METRES = 0.9
    OFFLOADS = 100
    LINE_BREAK_ASSISTS = 10
    KICK_METRES = 0.05
    TRY_ASSISTS = 8
    DECOY_RUNS = 20
    DUMMY_HALF_RUNS = 10
    MISSED_TACKLES = -10
    CHARGE_DOWNS = 100
    INTERCEPTS = 100
    ERRORS = -10
    INEFFECTIVE_TACKLES = -10
    PENALTIES_CONCEDED = -10
    HANDLING_ERRORS = -10
    SHORT_DROPOUTS = -10
    FOURTY_TWENTY_KICKS = 20
    KICK_RETURN_METRES = 0.10
    TACKLES = 0.02
    FIELD_GOALS = 60
    RUNS = 0.010
    KICKS = 5
    CONVERSION_PERCENT = 2
  
  
def set_games_played(stats):
    Played = stats.get("PLAYED", 0)
    Played_nerf = (Played - Played * 2)
    return Played_nerf

    
def calculate_score(team_stats):
    '''
    Calculate the score for a team based on their statistics
    '''
    score = 0
    total_games_played = team_stats.get("PLAYED", 0) 
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
                logger.warning(f"NaN value encountered for statistic: {stat}")
                continue

            try:
                value_float = float(value_str)

                score += value_float * weight
            except ValueError:
                logger.warning(f"Could not convert value: {value} for statistic: {stat}")
        else:
            logger.warning(f"Ignoring unmapped statistic: {stat}")

    # Dynamic adjustment for PLAYED statistic
    set_games_played(team_stats) 
    if total_games_played > 0:
        score += 7000 * ScoringRules.PLAYED.value
        
    if completion_rate > completion_rate_threshold:
        score += ScoringRules.COMPLETION_RATE.value * (completion_rate - completion_rate_threshold)
    logger.warning(f"Calculated score: {score}")
    return score

def compare_teams(team_data, team1_name, team2_name):
    team1_data = team_data.loc[team1_name].to_dict()
    team2_data = team_data.loc[team2_name].to_dict()

    team1_score = calculate_score(team1_data)
    team2_score = calculate_score(team2_data)

    return team1_name if team1_score > team2_score else team2_name if team2_score > team1_score else "Tie"
