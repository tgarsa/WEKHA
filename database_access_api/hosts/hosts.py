# Access to our how Library
# TODO: Look for an alternative import to won't see this error.
from utils import database, network, time
from etls.normalize import normalize

# Access to the Postgres database
import psycopg2
from numpy import int64
# from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(int64, psycopg2.extensions.AsIs)

# Define the connection
# We won't close the connection; we will continue using.
# Build the connection from the adequate data.
connection = psycopg2.connect(
    host=network.ip,
    port=5432,
    database=database.database,
    user=database.user,
    password=database.password
)


def _locate_id(id):
    '''
    Look for possible IDs that start with the same letters. After we will count how many possible duplicates to sum one
    and add in the three-number format to the ID.
    We look for the ID into the silver layer, players table.
    :param id: The letters of the ID, from the name and surname.
    :return: The number of possible duplicates.
    '''
    sql = "select id_sede from sedes where id_sede LIKE '{}%'".format(id)
    # Connect to the database
    cursor = connection.cursor()
    cursor.execute(sql)
    cuantos = cursor.rowcount
    cursor.close()
    return cuantos


def _new_id(provincia):
    '''
    WE buils the new ID, after to do a search into the database.
    :param provincia:
    :return: the new ID
    '''
    new_id = ''
    for name in provincia.split(' '):
        new_id += name.capitalize()
    new_id += f'{_locate_id(new_id) + 1:03d}'
    return new_id


def add(sede):
    '''
    To add a new SEDE into the database.
    :param sede: Hosts' data.
    :return: Explanatory text.
    '''

    # Access to the database
    # cursor = connection.cursor()

    for cont in range(sede.shape[0]):
        data = sede.iloc[cont]
        # Now, we build the internal data, "id_sede", and "created_at"
        # Build the new_id.
        data['id_sede'] = _new_id(data['provincia'])
        # Catch the time
        data['created_at'] = time.now()
        data['updated_at'] = data['created_at']
        data_norm = normalize(data.copy())
        # exit_text = _add_sede(cursor, data_norm)
        exit_text = database.add(data_norm, 'sedes')
        # connection.commit()

    return exit_text


# def _update_sede(cursor, df):
#     '''
#     Here, we update the data's sede
#     :param cursor: Connection to the database
#     :param data_norm: Data tu update, + sede ID
#     :return: Explanatory text.
#     '''
#     id_jugador = df['id_sede']
#     df.drop('id_sede', inplace=True)
#
#     # Building the sql to update the data in the Silver Layer.
#     sql = 'UPDATE sedes SET'
#
#     for count, column in enumerate(df.index):
#         if count > 0:
#             sql += ','
#         sql += f" {column} = '{df[column]}'"
#     sql += f" WHERE id_sede = '{id_jugador}'"
#     # Execute SQL
#     cursor.execute(sql)
#     return {'label': 'Done It'}


def update(sede):
    '''
    This function update the data contained into the database using the 'id_jugador' as key.
    :param sede: This will contain the 'id_sede' to know which player we will to modify and the rest of the fields will
     contain the new data.
    :return: Explanatory text.
    '''

    columns = list(sede)
    # # Start the cursor.
    # cursor = connection.cursor()

    # First add the timestamp to the DF.
    sede['updated_at'] = time.now()
    data = sede.iloc[0]
    data_norm = normalize(data.copy())
    cuantos = _locate_id(data['id_sede'])
    if cuantos == 1:
        # Update the data in the silver layer
        # exit_text = _update_sede(cursor, data_norm)
        exit_text = database.update(data, 'sedes', 'id_sede')
        # Commit the data
        # connection.commit()
    else:
        exit_text = {"label": 'El identificador de la SEDE es incorrecto'}

    # Close the cursor
    # cursor.close()

    return exit_text


def get(df):
    '''
        Download the data of a sede looking for the features passed in the KWARGS.
        :param df: Set of features that we will use to download the data.
        :return: The data of a player.
        '''

    # data =
    return database.get(df, 'sedes')