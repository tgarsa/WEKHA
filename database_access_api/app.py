# In this package, we only define the end points.

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from pandas import read_json
from io import StringIO

# importing the methods to communicate with the database
import players.players as players
import hosts.hosts as hosts

from psycopg2.extensions import register_adapter, AsIs
register_adapter(np.int64, AsIs)


# To be sure that the customer send the data in teh correct format.
# I will need to add more styles.
class Input(BaseModel):
    df_json: str


# Defining our API
app = FastAPI(title="Database Access",
              description="A simple api to connect with the database to have the WEHKA data.",
              version="0.1")


# Access to the players tables.
@app.post('/new_player', tags=["LoadPlayers"])
async def new_player(incoming_data: Input):
    df = read_json(StringIO(incoming_data.df_json))
    result = players.add(df)
    return result


@app.post('/update_player', tags=["UpdatePlayer"])
async def update_player(incoming_data: Input):
    df = read_json(StringIO(incoming_data.df_json))
    result = players.update(df)
    return result


@app.get('/get_player', tags=["GetPlayer"])
async def get_player(incoming_data: Input):
    df = read_json(StringIO(incoming_data.df_json))
    result = players.get(df)
    return result


# Access to the sedes tables.
@app.post('/new_sede', tags=["LoadHosts"])
async def new_sede(incoming_data: Input):
    df = read_json(StringIO(incoming_data.df_json))
    result = hosts.add(df)
    return result


@app.post('/update_sede', tags=["UpdateHosts"])
async def update_sede(incoming_data: Input):
    df = read_json(StringIO(incoming_data.df_json))
    result = hosts.update(df)
    return result


@app.get('/get_sede', tags=["GetHosts"])
async def get_sede(incoming_data: Input):
    df = read_json(StringIO(incoming_data.df_json))
    result = hosts.get(df)
    return result
