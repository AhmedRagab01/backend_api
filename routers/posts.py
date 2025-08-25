from fastapi import Depends,status, HTTPException,Response, APIRouter
from database import get_db_session
from schemas import Posts,Posts_response
from database_models import Posts_table
from sqlalchemy.orm import Session 

## is a way to use routers instead of actually app to register endpoints in different files for better structure
## prefix to say each end point starts with /posts resource just add the remaining url in the function 
posts_router = APIRouter(prefix= '/posts',
                         tags= ['Posts_Group']) ## Tags are only for documentation purposes to group each router's endpoints

@posts_router.get('')
def get_all_posts(db_session : Session =  Depends(get_db_session)):

    ## note this is lazy evaluation means no SQL is executed until .all() or any action is used to execute the query plan
    Query_object = db_session.query(Posts_table) ## just draw the SQL query plan and saved as Query object
    all_posts = Query_object.all() 
    print(type(all_posts[0]))

    return all_posts ## fastapi automatically seriallize this to JSON to send it back as a response



@posts_router.post('',status_code= status.HTTP_201_CREATED, response_model=Posts_response) ## this tells fastapi to set the default status to response 201 if it run successfully
def insert_posts(post: Posts, db_session: Session = Depends(get_db_session)):

    # new_post_object = Posts_table(title = post.title, content = post.content, published = post.published) ## new post object
    new_post_object = Posts_table(**post.dict()) ## use this if your pydantic schema's fields names same as table's columns names

    db_session.add(new_post_object) ## just a query object to draw SQL insert statment into the db table , it knows which table from the type of 
    db_session.commit() ## to commit the changes to DB
    db_session.refresh(new_post_object) ## it's like a refresh on the python object by retreiving this row values after inserting it

    return new_post_object ## will return only the title & content as per the response schema 

@posts_router.get('/{id}')
def get_post(id: int,db_session: Session = Depends(get_db_session)):
    Query_object = db_session.query(Posts_table).filter(Posts_table.id == id) ## just draw the SQL query plan and saved as Query object
    post_required = Query_object.first()
    if post_required == None:
        raise HTTPException(status_code=404, detail="Post not found!!")
    return post_required

@posts_router.delete('/{id}')
def delete_post(id: int,db_session: Session = Depends(get_db_session)):
    ## here to delete a row we first have to query it to get it as an object then do delete statment on it 
    ## all these arent executed its just sql query planning until using commit()
    post_to_delete_query = db_session.query(Posts_table).filter(Posts_table.id == id)
    post_object = post_to_delete_query.first()
    if post_object == None:
        raise HTTPException(status_code=404, detail="Post not found!!")
    post_to_delete_query.delete()
    db_session.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT) ## returning Response object 

@posts_router.put('/{id}')
def change_post(id: int, post: Posts,db_session: Session = Depends(get_db_session)):

    post_query = db_session.query(Posts_table).filter(Posts_table.id == id)

    post_itself =  post_query.first()
    if post_itself == None:
        raise HTTPException(status_code=404, detail="Post not found!!")
    ## updating
    post_query.update(post.dict(exclude_unset=True)) ## exclude_unset --> avoids overwriting existing values with None when they weren’t included in the request.
    db_session.commit()

    return post_query.first() 