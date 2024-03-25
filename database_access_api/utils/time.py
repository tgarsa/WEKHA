# In this, file we defined the functions to help us to load the time stamp correctly.

# We import the datetime package to load the fields created_at and modified_at
from datetime import datetime


def now():
    '''
    Return the current time in UTC time zone.
    :return: the timestamp
    '''
    return datetime.utcnow()
