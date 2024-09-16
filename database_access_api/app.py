# Here only define the end points.
import numpy as np
import fastapi
from fastapi import FastAPI
from pydantic import BaseModel
from pandas import read_json
from io import StringIO

# Tested FORM
# from src.model import spell_number
import jinja2
from fastapi import Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
# End Test

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
              version="0.1"
              )
# app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# templates = Jinja2Templates(directory='templates', autoescape=False, auto_reload=True)


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

# Tested the access from the Notebooks.
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

# Tested WEBSITE
# Tested FORM
@app.get('/')
def read_root():
    cual = fastapi.__version__
    return f'Hola MUNDO: {cual}'


@app.get("/form",
         response_class=HTMLResponse)
def form_post(request: Request):
    result = "Type a number"
    # print(result)
    # print(os.path.abspath(os.path.expanduser('templates')))
    # print('Tomasada')
    return templates.TemplateResponse(request=request,
                                      name="form.html",
                                      context={'result': result}
                                      )

@app.post("/form",
          response_class=HTMLResponse)
def form_post(request: Request,
              num: int = Form(...)
              ):
    result = f'Esto es una prueba de adivinación: {num}'
    return templates.TemplateResponse(request=request,
                                      name="form.html",
                                      context={'result': result}
                                      )


@app.get(path="/index",
         response_class=HTMLResponse
         )
def index(request: Request):
    return templates.TemplateResponse(request=request,
                                      name="index.html",
                                      #context={'result': result}
                                      )


@app.get(path="/admin",
         response_class=HTMLResponse
         )
def index(request: Request):
    return templates.TemplateResponse(request=request,
                                      name="admin.html",
                                      context={'result': ''}
                                      )


@app.post("/admin",
          response_class=HTMLResponse)
def form_post(request: Request,
              user: str = Form(...),
              password: str = Form(...),
              ):
    result = f'{user}: {password}'
    return templates.TemplateResponse(request=request,
                                      name="admin.html",
                                      context={'result': result}
                                      )

# Form to load the new players
@app.get(path="/players",
         response_class=HTMLResponse
         )
def players_new(request: Request):
    return templates.TemplateResponse(request=request,
                                      name="players_new.html"
                                      )

@app.get(path="/style",
         response_class=HTMLResponse
         )
def style(request: Request):
    print(type(request))
    print(request)
    return templates.TemplateResponse(request=request,
                                      name="style.css"
                                      )

@app.get(path="/navegacion",
         response_class=HTMLResponse
         )
def navegacion(request: Request):
    return templates.TemplateResponse(request=request,
                                      name="navegador_players.js"
                                      )

@app.get(path="/acciones",
         response_class=HTMLResponse
         )
def acciones(request: Request):
    return templates.TemplateResponse(request=request,
                                      name="acciones_new.js"
                                      )

@app.get(path="/jinja",
         response_class=HTMLResponse
         )
def jinja(request: Request):
    return templates.TemplateResponse(request=request,
                                      name="Jinja.html",
                                      context={"id": 345}
                                      )
