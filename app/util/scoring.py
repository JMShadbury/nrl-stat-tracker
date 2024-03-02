from util.logger import get_logger

logger = get_logger()

from enum import Enum

class ScoringRules(Enum):
    TRIES = 10
    GOALS = 2
    LINE_ENGAGED = 3
    COMPLETION = 20
    SUPPORT = 3
    LINE_BREAKS = 8
    POST_CONTACT_METRES = 5
    TACKLE_BREAKS = 5
    RUN_METRES = 0.001
    OFFLOADS = 8
    LINE_BREAK_ASSISTS = 8
    KICK_METRES = 0.01
    TRY_ASSISTS = 8
    DECOY_RUNS = 3
    DUMMY_HALF_RUNS = 7
    MISSED_TACKLES = -10
    CHARGE_DOWNS = 10
    INTERCEPTS = 9
    ERRORS = -10
    INEFFECTIVE_TACKLES = -10
    PENALTIES_CONCEDED = -10
    HANDLING_ERRORS = -10
    SHORT_DROPOUTS = 0
    FOURTY_TWENTY_KICKS = 10
    KICK_RETURN_METRES = 1
    FIELD_GOALS = 10
    RUNS = 0.001
    KICKS = 0.1
  
  
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


    return score