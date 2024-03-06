""" This module contains default values for the web scraping process. """

# pylint: disable=C0303
# pylint: disable=C0301
# pylint: disable=C0304
# pylint: disable=C0115

from enum import Enum


class TeamDefaults(Enum):
    TEAMS_PATH            = '//tbody[@class="table-tbody u-white-space-no-wrap"]'
    TEAMS_CONTAINER_TAG   = 'tbody'
    TEAMS_CONTAINER_CLASS = 'table-tbody u-white-space-no-wrap'
    TEAMS_ELEMENT_SELECT  = 'tr.table-tbody__tr'
    TEAMS_ROW_TAG         = 'span'
    TEAMS_ROW_CLASS       = 'u-font-weight-600'
    
class RoundDefaults(Enum):
    MATCH_PATH            = '//div[contains(@class, "match o-rounded-box o-shadowed-box")]'
    MATCH_CLASS_TAG       = 'p'
    MATCH_CONTAINER_CLASS = 'match o-rounded-box o-shadowed-box match--pregame'
    HOME_TEAM_CLASS       = 'match-team__name match-team__name--home'
    AWAY_TEAM_CLASS       = 'match-team__name match-team__name--away'
    MATCH_URL_TAG         = 'a'
    MATCH_HREF            = 'href'
    MATCH_URL_CLASS       = 'match--highlighted'
    STADIUM_CLASS         = 'match-venue o-text'
    
class GameDefaults(Enum):
    GAME_PATH                       = '//div[@class="l-grid__cell l-grid__cell--100 l-grid__cell--padding-16 l-grid__cell--padding-24-at-960"]'
    GAME_PLAYED_TAG                 = 'p'
    GAME_PLAYED_CLASS               = 'match-centre-head-to-head__played'
    GAME_AWAY_WINS_TAG              = 'p'
    GAME_AWAY_WINS_CLASS            = 'match-centre-head-to-head__wins match-centre-head-to-head__wins--away'
    GAME_HOME_WINS_TAG              = 'p'
    GAME_HOME_WINS_CLASS            = 'match-centre-head-to-head__wins match-centre-head-to-head__wins--home'
    GAME_WINS_WINNER_CLASS          = ' u-font-weight-700'
    GAME_PREV_CONTAINER_TAG         = 'div'
    GAME_PREV_CONTAINER_CLASS       = 'match-header l-billboard-max-width'
    GAME_PREV_HOME_SCORE_TAG        = 'div'
    GAME_PREV_HOME_SCORE_CLASS      = 'match-team__score match-team__score--home'
    GAME_PREV_AWAY_SCORE_TAG        = 'div'
    GAME_PREV_AWAY_SCORE_CLASS      = 'match-team__score match-team__score--away'
    GAME_PREV_HOME_NAME_TAG         = 'p'
    GAME_PREV_AWAY_NAME_TAG         = 'p'
    GAME_PREV_HOME_NAME_CLASS       = 'match-team__name match-team__name--home'
    GAME_PREV_AWAY_NAME_CLASS       = 'match-team__name match-team__name--away'
    GAME_PREV_SCORE_WINNER_CLASS    = ' u-font-weight-300'