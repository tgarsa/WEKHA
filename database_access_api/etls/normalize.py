# In this package we will define the functions that we will use to normalize the data
from datetime import datetime

# Function to Capitalize the names
def _capitalize(input):
    '''
    Capitalize the Sapnish name, less the prepositions.
    :param input: Text to capitalize
    :return: Text capitalized.
    '''
    # Set of prepositions to don't need to capitalize.
    replace_text = {'Del': 'del',
                    'De': 'de',
                    'La': 'la'
                    }

    string = ' '.join(it.capitalize() for it in input.split(' '))
    for preposition in replace_text:
        string = string.replace(preposition, replace_text[preposition])
    return string


# Function to ensure that we only have numbers
def _numerize(string):
    '''
    We will delete all the characters that are not a number.
    :param string: The input string with ...
    :return: A new string without letters or punctuation.
    '''
    from re import sub
    return sub(r'[^0-9]', '', str(string))


def _norm_comment(table, id, comment):

    from utils.database import prev_comments
    from utils.time import date_string
    from pandas import isnull

    # Look for the previous comments.
    prev = prev_comments(table, id)[0]
    if isnull(prev):
        return_text = date_string() + ': ' + comment + ' \n '
    else:
        return_text = prev + date_string() + ': ' + comment + ' \n '
    return return_text

# Function to normalize the data
def normalize(df, table):
    '''
    We evaluate each field that will be necessary to normalize, and send the data the correct function.
    :param df: Player's data in a DataFrame format.
    :return: The DataFrame after to normalize
    '''
    for key in df.keys():
        if key in ['nombre', 'apellido', 'residencia', 'pais', 'edificio', 'provincia', 'localidad', 'ambito',
                   'dep_cont', 'per_cont']:
            df[key] = _capitalize(df[key])
        elif key in ['dni', 'telefono', 'tel_cont', 'numero']:
            df[key] = _numerize(df[key])
        elif key in ['email', 'email_cont']:
            df[key] = df[key].lower()
        elif key in ['observaciones']:
            df[key] = _norm_comment(table, df['id'], df[key])
        elif key in ['hasta']:
            df[key] = datetime.strptime(df[key], "%d/%m/%Y")
    return df

