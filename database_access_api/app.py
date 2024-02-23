import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

# import pandas as pd
from pandas import notnull, read_json
# to have access to PostgreSQL database
import psycopg2
from psycopg2.extensions import register_adapter, AsIs
register_adapter(np.int64, AsIs)

# importing the methods to communicate with the database
from players.players import _set

# To be sure that the customer send the data in teh correct format.
class Input(BaseModel):
    df_json: str

# Defnied our API
app = FastAPI(title="Database Access",
              description="A simple api to connect with the database to have the WEHKA data.",
              version="0.1")


# TODO: Tomorrow, I will need to delete all and add new functions in terms of the new dat sets.
# I like to working by areas.
# Access to the players tables.

@app.post('/load_players', tags=["LoadPlayers"])
async def post_product(incoming_data: Input):
    df = read_json(incoming_data.df_json)
    exit = _set(df)
    return {"label": exit}

