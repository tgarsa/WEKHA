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
    sql = "select id_jugador from jugadores where id_jugador LIKE '{}%'".format(id)
    # Connect to the database
    cursor = connection.cursor()
    cursor.execute(sql)
    cuantos = cursor.rowcount
    cursor.close()
    return cuantos


def _new_id(nombre, apellidos):
    '''
    Based in the name and the surname, and looking for posible repetition in the database
    :param nombre:
    :param apellidos:
    :return: A string in which the letters are the first letter of each name and surname, in upper case, and added a
            number to ensure that we don't have duplicate IDs
    '''
    new_id = ''
    for name in nombre.split(' '):
        new_id += name[:1].upper()
    for surname in apellidos.split(' '):
        new_id += surname[:1].upper()
    new_id += f'{_locate_id(new_id) + 1:03d}'
    return new_id


def _invalid_data(**kwargs):
    '''
    We evaluate if the fields shared in the arguments would be unique data into the database.
    :param kwargs: Fields that we will evaluate.
    :return: List of fields with values contained into the database. Null if the data is new.
    '''
    cursor = connection.cursor()
    return_text = ''
    for i in kwargs.items():
        sql = f"select {i[0]} from jugadores where {i[0]} LIKE '{i[1]}'"
        cursor.execute(sql)
        if i[0] != 'id_jugador':
            if cursor.rowcount > 0:
                return_text += f'{i[0]}, '
        else:
            if cursor.rowcount == 0:
                return_text += f'{i[0]}, '
    cursor.close()
    return return_text[:-2]


def _add_bronze_player(cursor, data):
    '''
    We saved here the data. Don't do anymore.
    :param cursor: The cursor to access to the database
    :param data: The dataframe with the whole of the data
    :return: Verification text.
    '''
    # SQL to write into the bronze layer
    # List Comprehension approach
    sql_bronze = "INSERT INTO jugadores_bronze ("
    sql_bronze += (', ').join(x for x in data.index)
    sql_bronze += ") values ("
    sql_bronze += (',').join('%s' for x in data.index)
    sql_bronze += ")"

    data_sec = tuple([f"{data[x]}" for x in data.index])

    cursor.execute(sql_bronze, data_sec)

    return "Bronze Layer: OK. "


def _add_player(cursor, data):
    '''
    We saved here the data. Don't do anymore.
    :param cursor: The cursor to access to the database
    :param data: The dataframe with the whole of the data
    :return: Verification text.
    '''

    # SQL to write into the bronze layer
    sql_silver = ("INSERT INTO jugadores (id_jugador, dni, nombre, apellidos, nick, email, telefono, "
                  "residencia, pais, talla, discapacidades, observaciones, created_at, updated_at) "
                  "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    cursor.execute(sql_silver, (data['id_jugador'], data['dni'], data['nombre'], data['apellidos'],
                                data['nick'], data['email'], data['telefono'], data['residencia'],
                                data['pais'], data['talla'], data['discapacidades'], data['observaciones'],
                                data['created_at'], data['created_at'])
                   )
    return "Silver Layer: OK. "


def add(player):
    '''
    We add the data of the player, only one player, into the database.
    First in the Bronze layer, and after to normalize into the Silver layer.
    :param player: DataFrame with the player's data.
    :return: Explanatory text.
    '''

    # Exit text
    exit_text = ''
    # Access to the database
    cursor = connection.cursor()

    for cont in range(player.shape[0]):
        data = player.iloc[cont]
        # Now, we build the internal data, "id_player", and "created_at"
        # Build the new_id.
        data['id_jugador'] = _new_id(data['nombre'], data['apellidos'])
        # Catch the time
        data['created_at'] = time.now()
        data_norm = normalize(data.copy())
        invalid_data_text = _invalid_data(dni=data_norm['dni'],
                                          email=data_norm['email'],
                                          telefono=data_norm['telefono'])
        if invalid_data_text == "":
            exit_text = _add_bronze_player(cursor, data)
            exit_text += _add_player(cursor, data_norm)
            exit_text = {"label": exit_text}
            connection.commit()
        else:
            exit_text = {"label": f'Los campos {invalid_data_text} tienen valores previamente almacenados.'}

    return exit_text


def get(df):
    '''
    Download the data of a player looking for the features passed in the KWARGS.
    :param df: Set of features that we will use to download the data.
    :return: The data of a player.
    '''

    # Start the connection.
    cursor = connection.cursor()
    # Start to build the SQL
    sql = "select * from jugadores where"

    for count, column in enumerate(df.columns):
        if count > 0:
            sql += ' and'
        if column == "email":
            sql += f" {column} = '{df.iloc[0][column].lower()}'"
        else:
            sql += f" {column} = '{df.iloc[0][column]}'"

    cursor.execute(sql)
    # Download the data
    data = cursor.fetchall()
    # Close the connection
    cursor.close()
    return data

def _update_player(cursor, df):
    '''
    Here, we update the data into the silver layer
    :param cursor: Connection to the database
    :param df: Data tu update, + player ID
    :return: Explanatory text.
    '''

    id_jugador = df['id_jugador']
    df.drop('id_jugador', inplace=True)

    # Building the sql to update the data in the Silver Layer.
    sql = 'UPDATE jugadores SET'

    for count, column in enumerate(df.index):
        if count > 0:
            sql += ','
        if column == 'created_at':
            sql += f" updated_at = '{df[column]}'"
        else:
            sql += f" {column} = '{df[column]}'"
    sql += f" WHERE id_jugador = '{id_jugador}'"
    # Execute SQL
    cursor.execute(sql)

    return "Silver Layer: OK. "



def update(df):
    '''
    This function update the data contained into the database using the 'id_jugador' as key.
    :param df: This will contain the 'id_jugador' to know which player we will to modify and the rest of the fields will
     contain the new data.
    :return: Explanatory text.
    '''

    columns = list(df)
    # Start the cursor.
    cursor = connection.cursor()

    # First add the timestamp to the DF.
    df['created_at'] = time.now()
    data = df.iloc[0]
    data_norm = normalize(data.copy())
    invalid_data_text = _invalid_data(id_jugador=data_norm['id_jugador'])
    if 'dni' in columns:
        if invalid_data_text != '':
            invalid_data_text += ', '
        invalid_data_text += _invalid_data(dni=data_norm['dni'])
    if 'email' in columns:
        if invalid_data_text != '':
            invalid_data_text += ', '
        invalid_data_text += _invalid_data(email=data_norm['email'])
    if 'telefono' in columns:
        if invalid_data_text != '':
            invalid_data_text += ', '
        invalid_data_text += _invalid_data(telefono=data_norm['telefono'])

    if invalid_data_text == "":
        # Save the data to update in the bronze layer
        exit_text = _add_bronze_player(cursor, data)
        # Update the data in the silver layer
        exit_text += _update_player(cursor, data_norm)
        exit_text = {"label": exit_text}
        # Commit the data
        connection.commit()
    else:
        exit_text = {"label": f'Los campos {invalid_data_text} tienen valores no validos.'}

    # Close the cursor
    cursor.close()

    return exit_text
