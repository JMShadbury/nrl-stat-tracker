
from enum import Enum


class TeamDefaults(Enum):
    TEAMS_PATH = '//tbody[@class="table-tbody u-white-space-no-wrap"]'
    TEAMS_FIND_TAG = 'tbody'
    TEAMS_FIND = 'table-tbody u-white-space-no-wrap'
    TEAMS_ELEMENT_SELECT = 'tr.table-tbody__tr'
    TEAMS_ROW_FIND_TAG = 'span'
    TEAMS_ROW_FIND = 'u-font-weight-600'
    
class RoundDefaults(Enum):
    MATCH_PATH = '//div[contains(@class, "match o-rounded-box o-shadowed-box match--pregame")]'
    MATCH_FIND_TAG = 'tbody'
    MATCH_FIND = 'table-tbody u-white-space-no-wrap'
    MATCH_ELEMENT_SELECT = 'tr.table-tbody__tr'
    MATCH_ROW_FIND_TAG = 'span'
    MATCH_ROW_FIND = 'u-font-weight-600'
