# Access to our how Library
# TODO: Look for an alternative import to won't see this error.
from utils import database, time
from etls.normalize import normalize

# Set of filed used to build id keys of each table
# "table": "field"
id_build = {
    # 'jugadores': tuple('nombre', 'apellidos'),
    'sedes': ('provincia', ),
    'licencias': ('ambito', ),
    'patrocinadores': ('nombre', ),
    'alojamientos': ('nombre', ),
    'patrocinios': ('id_patrocinador', 'id_campeonato'),
    'campeonatos': ('nombre', ),
    'campeonatos_arbitros': ('id_campeonato', 'id_arbitro'),
    'campeonatos_jugadores': ('id_campeonato', 'id_jugador'),
    'campeonatos_jugadas': ('id_campeonato', 'id_prueba', 'id_mesa', 'id_ronda'),
    'mesas': ('id_campeonato', 'fila', 'columna'),
    'pruebas': ('nombre', 'discapacidades'),
    'jugadores_campeonato': ('id_jugador', 'id_campeonato'),
    'jugadores_pruebas': ('id_jugador', 'id_campeonato', 'id_prueba', 'id_ronda')
}


def _new_id(table, keys):
    '''
    We build the new ID, after to do a search into the database.
    :param provincia:
    :return: the new ID
    '''
    new_id = ''
    for key in keys:
        if str(key).isdigit():
            new_id += str(key)
        else:
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
        if (column != 'id_table') and ('id_' in column):
            cuantos = database.check_id(column, data[column])
            if cuantos != 1:
                if count > 1:
                    exit_text += ', '
                exit_text += column
    return exit_text


def add(indata, table):
    '''
    To add a new SEDE into the database.
    :param data: Hosts' data.
    :param table: Table to use.
    :return: Explanatory text.
    '''
    # print(data)
    for cont in range(indata.shape[0]):
        data = indata.iloc[cont]
        result = _test_ids(data)
        if result == '':
            id_data = tuple(data[campo] for campo in id_build[table])
            data['id'] = _new_id(table, id_data)
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
