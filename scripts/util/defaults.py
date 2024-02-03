from enum import Enum


class Url(Enum):
    '''Enum class for URLs'''
    LADDER = "https://www.nrl.com/ladder/"
    TEAM_TRIES = "https://www.nrl.com/stats/teams/?competition=111&season=2023&stat=38"
    TEAM_POINTS = "https://www.nrl.com/stats/teams/?competition=111&season=2023&stat=76"
    TEAM_GOALS = "https://www.nrl.com/stats/teams/?competition=111&season=2023&stat=1000034"
    TEAM_LINE_ENGAGED = "https://www.nrl.com/stats/teams/?competition=111&season=2023&stat=1000025"
    TEAM_POSSESSION = "https://www.nrl.com/stats/teams/?competition=111&season=2023&stat=9"
