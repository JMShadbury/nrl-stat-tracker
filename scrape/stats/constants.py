""" This module contains default values for the web scraping process. """

# pylint: disable=C0303
# pylint: disable=C0301
# pylint: disable=C0304
# pylint: disable=C0115

from enum import Enum


class TeamDefaults(Enum):
    TEAMS_PATH = '//tbody[@class="table-tbody u-white-space-no-wrap"]'
    TEAMS_CONTAINER_TAG = 'tbody'
    TEAMS_CONTAINER_CLASS = 'table-tbody u-white-space-no-wrap'
    TEAMS_ELEMENT_SELECT = 'tr.table-tbody__tr'
    TEAMS_ROW_TAG = 'span'
    TEAMS_ROW_CLASS = 'u-font-weight-600'
