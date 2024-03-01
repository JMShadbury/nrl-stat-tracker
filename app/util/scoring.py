from util.logger import get_logger

logger = get_logger()

from enum import Enum

class ScoringRules(Enum):
    TRIES = 0.1
    POINTS = 0.05
    GOALS = 0.01
    LINE_ENGAGED = 0.02
    COMPLETION = 0.1
    SUPPORT = 0.3
    LINE_BREAKS = 0.5
    POST_CONTACT_METRES = 0.3
    TACKLE_BREAKS = 0.3
    RUN_METRES = 0.4
    RUNS = 0.1
    KICK_RETURN_METRES = 0.2
    OFFLOAD = 0.3
    LINE_BREAK_ASSISTS = 0.4
    KICKS = 0.1
    KICK_METRES = 0.3
    TRY_ASSISTS = 0.4
    CONVERSION_PERCENTAGE = 0.2
    ALL_RECEIPTS = 0.2
    FIELD_GOALS = 0.6
    DECOY_RUNS = 0.2
    DUMMY_HALF_RUNS = 0.2
    TACKLES = -0.01
    MISSED_TACKLES = -0.05
    CHARGE_DOWNS = 0.6
    INTERCEPTS = 0.8
    FORTY_TWENTY_KICKS = 0.6
    SHORT_DROPOUTS = -0.01
    ERRORS = -0.05
    INEFFECTIVE_TACKLES = -0.04
    PENALTIES_CONCEDED = -0.06
    HANDLING_ERRORS = -0.05
    
    
def calculate_score(team_stats):
    score = 0
    for stat, value in team_stats.items():
        formatted_stat = stat.replace(" ", "_").upper()

        if formatted_stat in ScoringRules.__members__:
            weight = ScoringRules[formatted_stat].value

            # Convert value to a string for processing, if necessary
            value_str = str(value)

            # Check if the value contains commas and remove them
            if ',' in value_str:
                value_str = value_str.replace(",", "")

            # Check if the value is NaN (not a number)
            if value_str == 'nan':
                # Optionally log or handle NaN value
                logger.warning(f"NaN value encountered for statistic: {stat}")
                continue  # Skip this statistic

            try:
                # Convert the (possibly modified) value back to float
                score += weight * float(value_str)
            except ValueError:
                # Optionally log or print a message that the value could not be converted
                logger.warning(f"Could not convert value: {value} for statistic: {stat}")
        else:
            logger.warning(f"Ignoring unmapped statistic: {stat}")

    return score



