# Access to our how Library
# TODO: Look for an alternative import to won't see this error.
from utils import database, time
from etls.normalize import normalize


def _new_id(provincia):
    '''
    We build the new ID, after to do a search into the database.
    :param provincia:
    :return: the new ID
    '''
    new_id = ''
    for name in provincia.split(' '):
        new_id += name.capitalize()
    # new_id += f"{_locate_id(new_id) + 1:03d}"
    cuantos = database.count_id('sedes', 'id_sede', f'{new_id}')
    new_id += f'{cuantos + 1:03d}'
    return new_id


def add(sede):
    '''
    To add a new SEDE into the database.
    :param sede: Hosts' data.
    :return: Explanatory text.
    '''

    for cont in range(sede.shape[0]):
        data = sede.iloc[cont].copy()
        # Now, we build the internal data, "id_sede", and "created_at"
        # Build the new_id.
        data['id_sede'] = _new_id(data['provincia'])
        # Catch the time
        data['created_at'] = time.now()
        data['updated_at'] = data['created_at']
        # Normalize the data
        data_norm = normalize(data)
        exit_text = database.add(data_norm, 'sedes')

    return exit_text


def update(sede):
    '''
    This function update the data contained into the database using the 'id_jugador' as key.
    :param sede: This will contain the 'id_sede' to know which player we will to modify and the rest of the fields will
     contain the new data.
    :return: Explanatory text.
    '''

    columns = list(sede)
    # First add the timestamp to the DF.
    sede['updated_at'] = time.now()
    data = sede.iloc[0].copy()
    data_norm = normalize(data)
    cuantos = database.count_id('sedes', 'id_sede', f"{data['id_sede']}")
    if cuantos == 1:
        exit_text = database.update(data_norm, 'sedes', 'id_sede')
    else:
        exit_text = {"label": 'El identificador de la SEDE es incorrecto'}
    return exit_text


def get(df):
    '''
        Download the data of a sede looking for the features passed in the df.
        :param df: Set of features that we will use to download the data.
        :return: The data of a player.
        '''
    return database.get(df, 'sedes')
