# In this package we will define the functions that we will use to normalize the data

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
    return sub(r'[^1-9]', '', str(string))


# Function to normalize the data
def normalize(df):
    '''
    We evaluate each fields that will be necessary to normalize, and send the data t the correct function.
    :param df: Player's data in a DataFrame format.
    :return: The DataFrame after to normalize
    '''
    for key in df.keys():
        if key in ['nombre', 'apellido', 'residencia', 'pais']:
            df[key] = _capitalize(df[key])
        elif key in ['dni', 'telefono']:
            df[key] = _numerize(df[key])
            print(df[key])
        elif key in ['email']:
            df[key] = df[key].lower()

    return df

