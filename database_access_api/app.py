import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from pandas import read_json

# importing the methods to communicate with the database
import players.players

from psycopg2.extensions import register_adapter, AsIs
register_adapter(np.int64, AsIs)


# To be sure that the customer send the data in teh correct format.
class Input(BaseModel):
    df_json: str


# Defining our API
app = FastAPI(title="Database Access",
              description="A simple api to connect with the database to have the WEHKA data.",
              version="0.1")


# TODO: Tomorrow, I will need to delete all and add new functions in terms of the new dat sets.
# I like to working by areas.
# Access to the players tables.

@app.post('/new_player', tags=["LoadPlayers"])
async def new_player(incoming_data: Input):
    df = read_json(incoming_data.df_json)
    result = players.players.set(df)
    return result
