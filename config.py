# This file is to define a schema for our Environment variables to avoid hard coding them in the code
# and using pydantic helps to set a schema to make sure every configuration is defined already

from pydantic_settings import BaseSettings


## best practise to use capital letters as ENV Variables
class Settings(BaseSettings):
    DB_HOST :str 
    DB_PORT: int = 5432
    DB_TYPE: str = 'postgresql' ## Default value making it optional to set
    DB_USERNAME: str
    DB_PSWD: str
    DB_NAME: str

    class Config:
        env_file = ".env"


settings = Settings() ## to create a settings object


###  HOW IT WORKS ? ###

# 1. You create an object of this class
# 2. First Pydantic start searching in your environment variables in your system using os.environ for each field in the class.
# 3. If there is no env variable, it searches for the .env file for these fields values.
# 4. IF there is no env varb or in the .env file they take the default value if set in the class
# 5. we use the .env file only for development & use environmanetal variables in the production "so dont include .env in the git use .gitignore"