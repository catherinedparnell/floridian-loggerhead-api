import constants

def produce_egg_time(days_second, unit_time):
    seconds_days = constants.SECONDS / days_second
    return seconds_days * unit_time

def produce_turtle_time(days_second, unit_time):
    seconds_days = constants.SECONDS / days_second
    year_seconds = seconds_days * constants.YEAR_DAYS
    return year_seconds * unit_time