### This file contains schemas for any Request/Response Body.

from pydantic import BaseModel


class Posts(BaseModel):
    title : str
    content : str 
    published : bool = True

    ## this is to tell pydantic to expect other objects than just dictionary to validate its values
    ## since in normal dicts it try to get values like this dict['title']
    ## but in case it deals with a class like an ORM class it have to try to access its fields like class.title 
    ## Usually used to put a schema for a Response
    class Config:
        orm_mode = True


class Posts_response(BaseModel):
    
    title : str
    content : str 

    class Config:
        orm_mode = True
