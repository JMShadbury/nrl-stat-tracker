
from enum import Enum
 
class TeamDefaults(Enum):
    POINTS_TABLE_ELEMENT = '//tbody[@class="table-tbody u-white-space-no-wrap"]'
    POINTS_ELEMENT_TYPE  = 'tbody'
    POINTS_ELEMENT       = 'tr.table-tbody__tr'
    TRIES_TABLE_ELEMENT  = '//tbody[@class="table-tbody u-white-space-no-wrap"]'
    TRIES_ELEMENT_TYPE   = 'tbody'
    TRIES_ELEMENT        = 'tr.table-tbody__tr'
    