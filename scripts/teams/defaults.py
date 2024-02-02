
from enum import Enum
 
class TeamDefaults(Enum):
    TEAMS_PATH           = '//tbody[@class="table-tbody u-white-space-no-wrap"]'
    TEAMS_FIND_TAG       = 'tbody'
    TEAMS_FIND           = 'table-tbody u-white-space-no-wrap'
    TEAMS_ELEMENT_SELECT = 'tr.table-tbody__tr'
    TEAMS_ROW_FIND_TAG   = 'span'
    TEAMS_ROW_FIND       = 'u-font-weight-600'
    