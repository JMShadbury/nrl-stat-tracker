from util.logger import get_logger

logger = get_logger()

from enum import Enum

class ScoringRules(Enum):
    PLAYED = -5
    TRIES = 10
    POINTS = 5
    GOALS = 2
    LINE_ENGAGED = 3
    COMPLETION = 20
    SUPPORT = 3
    LINE_BREAKS = 20
    POST_CONTACT_METRES = 0.8
    TACKLE_BREAKS = 3
    RUN_METRES = 0.01
    OFFLOAD = 15
    LINE_BREAK_ASSISTS = 2
    KICK_METRES = 0.2
    TRY_ASSISTS = 8
    DECOY_RUNS = 3
    DUMMY_HALF_RUNS = 4
    MISSED_TACKLES = -5
    CHARGE_DOWNS = 20
    INTERCEPTS = 9
    ERRORS = -10
    INEFFECTIVE_TACKLES = 8
    PENALTIES_CONCEDED = -10
    HANDLING_ERRORS = -5
    SHORT_DROPOUTS = 5
    FOURTY_TWENTY_KICKS = 5
    KICK_RETURN_METRES = 3
    FIELD_GOALS = 5
    RUNS = 0.2
    KICKS = 2
    
    
def calculate_score(team_stats):
    '''
    Calculate the score for a team based on their statistics
    '''
    score = 0
    total_games_played = team_stats.get("PLAYED", 0)
    completion_rate = team_stats.get("COMPLETION_RATE", 0)
    completion_rate_threshold = 75 

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

                if formatted_stat != "PLAYED":
                    # Normalize other stats based on games played
                    if total_games_played > 0:
                        value_float /= total_games_played

                score += weight * value_float
            except ValueError:
                logger.warning(f"Could not convert value: {value} for statistic: {stat}")
        else:
            logger.warning(f"Ignoring unmapped statistic: {stat}")

    # Dynamic adjustment for PLAYED statistic
    if total_games_played > 0:
        played_weight_adjustment = (total_games_played / 24) ** 0.5 
        score += ScoringRules.PLAYED.value * played_weight_adjustment
        
    if completion_rate > completion_rate_threshold:
        score += ScoringRules.COMPLETION_RATE.value * (completion_rate - completion_rate_threshold)


    return score