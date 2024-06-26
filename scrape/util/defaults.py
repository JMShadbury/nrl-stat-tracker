"""Module containing URL enumeration."""

from enum import Enum


class Url(Enum):
    '''Enum class for URLs'''

    # Ladder
    LADDER = "https://www.nrl.com/ladder/"

    # Teams
    TEAM_TRIES = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=38"
    TEAM_POINTS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=76"
    TEAM_GOALS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=1000034"
    TEAM_LINE_ENGAGED = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=1000025"
    TEAM_POSSESSION = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=9"
    TEAM_COMPLETION = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=1000210"
    TEAM_SUPPORT = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=1000015"
    TEAM_LINE_BREAKS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=30"
    TEAM_POST_CONTACT_METRES = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=1000112"
    TEAM_TACKLE_BREAKS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=29"
    TEAM_ALL_RUN_METRES = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=1000037"
    TEAM_ALL_RUNS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=1000038"
    TEAM_KICK_RETURN_METRES = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=78"
    TEAM_OFFLOADS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=28"
    TEAM_LINE_BREAK_ASSISTS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=31"
    TEAM_TOTAL_KICKS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=33"
    TEAM_TOTAL_KICK_METRES = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=32"
    TEAM_TRY_ASSISTS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=35"
    TEAM_CONVERSION_PERCENT = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=1000209"
    TEAM_ALL_RECEIPTS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=1000028"
    TEAM_FIELD_GOALS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=69"
    TEAM_DECOY_RUNS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=1000002"
    TEAM_DUMMY_HALF_RUNS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=81"
    TEAM_TACKLES = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=3"
    TEAM_MISSED_TACKLES = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=4"
    TEAM_CHARGE_DOWNS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=1000000"
    TEAM_INTERCEPTS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=1000004"
    TEAM_40_20_KICKS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=82"
    TEAM_SHORT_DROPOUTS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=1000415"
    TEAM_ERRORS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=37"
    TEAM_INEFFECTIVE_TACKLES = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=1000003"
    TEAM_PENALTIES_CONCEDED = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=1000026"
    TEAM_HANDLING_ERRORS = "https://www.nrl.com/stats/teams/?competition=111&season=2024&stat=1000079"
    

    # Draw
    DRAW = "https://www.nrl.com/draw/?competition=111&round={round}&season=2024"

    @staticmethod
    def get_draw_url(round_number):
        """Get the URL for the draw for a specific round."""
        return Url.DRAW.value.format(round=round_number)
