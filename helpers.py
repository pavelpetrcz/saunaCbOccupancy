import time


def isTimeframeAroundWholeHour():
    """
    return True if time is between XX:00 and XX:05
    :return: boolean
    """
    minutes = time.localtime().tm_min
    return True if minutes in range(55, 2) else False
