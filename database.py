from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from config import settings
####    url --> <db_type>+<driver>://<username>:<password>@<host:port>/<database_name> #####

# DB_URL = "postgresql+psycopg2://postgres:ragabola11@localhost:5432/fastapi"           ### ## local URL

DB_URL =  f'{settings.DB_TYPE}://{settings.DB_USERNAME}:{settings.DB_PSWD}@{settings.DB_HOST}/{settings.DB_NAME}?sslmode=require&channel_binding=require'

engine = create_engine(url = DB_URL
                       , pool_size=3
                       , pool_pre_ping=True) ## to check if connection is available before using

session_object = sessionmaker(bind= engine) ## session maker object used to create sessions 

Base_model = declarative_base() ## this is the class object to inherrit from to define tables models/schemas

def get_db_session():

    db = session_object()  

    try:
        yield db ## pause function execution to return the db session

    finally:
        db.close() ## close the session after request is done 

    


    

    

