# In this file, we defined the functions to help us to load the time stamp correctly.

# We import the datetime package to load the fields created_at and modified_at
from datetime import datetime


def now():
    '''
    Return the current time in the UTC time zone.
    :return: the timestamp
    '''
    return datetime.utcnow()


def date_string():
    '''
    Return the day after to transforme in a string
    :return:  with the date
    '''
    return now().strftime("%d/%m/%y")
    # return datetime.utcnow().strftime("%d/%m/%y")
