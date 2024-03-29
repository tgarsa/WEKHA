# Access to our how Library
# TODO: Look for an alternative import to won't see this error.
from utils import database, time
from etls.normalize import normalize

# Set of filed used to build id keys of each table
# "table": "field"
id_build = {
    # 'jugadores': tuple('nombre', 'apellidos'),
    'sedes': 'provincia',
    'licencias': 'ambito',
    'patrocinadores': 'nombre',
    'alojamientos': 'nombre',
    'patrocinios': ('id_patrocinador', 'id_campeonato')
}


def _new_id(table, keys):
    '''
    We build the new ID, after to do a search into the database.
    :param provincia:
    :return: the new ID
    '''
    new_id = ''
    if type(keys) == str:
        for name in keys.split(' '):
            new_id += name.capitalize()
    elif type(keys) == tuple:
        for key in keys:
            for name in key.split(' '):
                new_id += name.capitalize()
    cuantos = database.count_id(table, f'{new_id}')
    new_id += f'{cuantos + 1:03d}'
    return new_id


def _test_ids(data):
    '''
    Tested if the connected IDs are in the database
    :param data:
    :param table:
    :return:
    '''
    exit_text = ''
    for count, column in enumerate(data.index):
        # TODO: Delete the additional condition when I would have data in the table.
        if (column != 'id_table') and ('id_' in column) and (column != 'id_campeonato'):
            cuantos = database.check_id(column, data[column])
            if cuantos != 1:
                if count > 1:
                    exit_text += ', '
                exit_text += column
    return exit_text


def add(data, table):
    '''
    To add a new SEDE into the database.
    :param data: Hosts' data.
    :param table: Table to use.
    :return: Explanatory text.
    '''
    for cont in range(data.shape[0]):
        data = data.iloc[cont].copy()
        result = _test_ids(data)
        if result == '':
            # Now, we build the internal data, "id", and "created_at"
            # Build the new_id.
            if table in id_build.keys():
                if type(id_build[table]) == tuple:
                    pas_data = tuple(data[campo] for campo in id_build[table])
                else:
                    pas_data = data[id_build[table]]
                data['id'] = _new_id(table, pas_data)
            # Catch the time
            data['created_at'] = time.now()
            data['updated_at'] = data['created_at']
            # Normalize the data
            data_norm = normalize(data, table)
            exit_text = database.add(data_norm, table)
        else:
            exit_text = f"Los identificadore {result} no estan en la base de datos"

    return exit_text


def update(data, table):
    '''
    This function updates the data contained into the database using the 'id' as key.
    :param data: This will contain the 'id_sede' to know which player we will to modify and the rest of the fields will
     contain the new data.
    :param table: Table to use.
    :return: Explanatory text.
    '''

    # Adding the timestamp to the DF.
    data['updated_at'] = time.now()
    data = data.iloc[0].copy()
    data_norm = normalize(data, table)
    cuantos = database.count_id(table, f"{data_norm['id']}")
    if cuantos == 1:
        exit_text = database.update(data_norm, table)
    else:
        exit_text = {"label": f'El identificador clave de la {table} es incorrecto'}
    return exit_text


def get(df, table):
    '''
        Download the data of a sede looking for the features passed in the df.
        :param df: Set of features that we will use to download the data.
        :return: The data of a player.
        '''
    # return database.get(df, 'sedes')
    return database.get(df, table)
