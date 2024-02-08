from util.logger import get_logger

logger = get_logger()
logger.setLevel("DEBUG")


def process_table_row(row, stat):
    '''
    Process a table row
    :param row: The table row to process
    :param stat: The statistic to process
    :return: The processed data
    '''
    logger.debug("Processing table row line engaged: {}".format(row))
    played = row.select_one('td:nth-of-type(4)').get_text(strip=True)
    goals = row.select_one('td:nth-of-type(5)').get_text(strip=True)

    data = {
        'TeamName': row.select_one('span.u-font-weight-600').get_text(strip=True),
        'Played': played,
        stat: goals
    }
    logger.debug("Processed data: {}".format(data))
    return data
