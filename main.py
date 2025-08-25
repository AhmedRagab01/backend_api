from fastapi import FastAPI
from database import Base_model,engine
from routers.posts import posts_router
from fastapi.middleware.cors import CORSMiddleware

### Sql alchemy doesnt know how to connect to a db so it need a driver like psycopg to be installed to work on top of it

# conn = psycopg.connect(host = "localhost", dbname="fastapi", user="postgres", password="ragabola11",row_factory=dict_row)

app = FastAPI()

## examples of how to define origin domains
origins = [
    "http://localhost:3000",   # React/Vue dev server
    "https://myfrontend.com",  # Production frontend
]

origins = ["*"] ## TO ALLOW  ALL DOMAINS


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # only allow listed origins
    allow_credentials=True,       # allow cookies/Authorization headers
    allow_methods=["*"],          # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],          # allow all headers
)




## this line to create all tables from the clases inherts from the base_model class
## this shouldn't be used in production instead use alembic to do database migrations and building database sctructure "should be removed after using alembic engine"
Base_model.metadata.create_all(bind=engine) 

@app.get('/')
def root():
    return {"Helloo world !"}


app.include_router(posts_router)