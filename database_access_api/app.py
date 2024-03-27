# Here only define the end points.
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from pandas import read_json
from io import StringIO

# To add security
from datetime import timedelta
import security as sec
from typing_extensions import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
# from typing import Any, Union

# importing the methods to communicate with the database
import players.players as players
import miscelanea.miscelanea as hosts


# To be sure that the customer send the data in the correct format.
class Input2(BaseModel):
    df_json: str


class Input(BaseModel):
    df_json: str
    table: str


# Defining our API
app = FastAPI(title="Database Access",
              description="A simple api to connect with the database to obtain the WEKHA data.",
              version="0.1")


# Security
@app.post("/token", response_model=sec.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = sec.authenticate_user(sec.fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=sec.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = sec.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Access to the players tables.
@app.post('/new_player',
          tags=["LoadPlayers"]
          )
async def new_player(incoming_data: Input2,
                     current_user: Annotated[sec.User, Depends(sec.get_current_active_user)]
                     ):
    df = read_json(StringIO(incoming_data.df_json))
    result = players.add(df)
    return result


@app.post('/update_player',
          tags=["UpdatePlayer"]
          )
async def update_player(incoming_data: Input2,
                        current_user: Annotated[sec.User, Depends(sec.get_current_active_user)]
                        ):
    df = read_json(StringIO(incoming_data.df_json))
    result = players.update(df)
    return result


# Miscelanea Access to the tables.
@app.post('/new')
async def new(incoming_data: Input,
              current_user: Annotated[sec.User, Depends(sec.get_current_active_user)]
              ):
    df = read_json(StringIO(incoming_data.df_json))
    result = hosts.add(df, incoming_data.table)
    return result


@app.post('/update')
async def update(incoming_data: Input,
                 current_user: Annotated[sec.User, Depends(sec.get_current_active_user)]
                 ):
    df = read_json(StringIO(incoming_data.df_json))
    result = hosts.update(df, incoming_data.table)
    return result


@app.get('/get')
async def get(incoming_data: Input,
              current_user: Annotated[sec.User, Depends(sec.get_current_active_user)]
              ):
    df = read_json(StringIO(incoming_data.df_json))
    result = hosts.get(df, incoming_data.table)
    return result
