from fastapi import APIRouter,status,HTTPException,Response
from typing import Optional
from fastapi.params import Body
from random import randrange
from config.database import cursor,connect
from model.list import Activity

router  = APIRouter()

# get
@router.get('/list')
def get_list():
    cursor.execute("""SELECT * FROM list """)
    activities = cursor.fetchall()
    return {'data':activities}

# post activities
@router.post('/create',status_code=status.HTTP_201_CREATED)
def create_activities(activity:Activity):
    cursor.execute("""INSERT INTO list (title, time, description, type, state) VALUES (%s, %s, %s, %s, %s) RETURNING * """,(activity.title,activity.time,activity.description,activity.type,activity.state))
    new_post = cursor.fetchone()
    connect.commit()
    return {'data':new_post}

# get activity by id
@router.get('/activity/{id}')
def get_activity_by_id(id:int):
    cursor.execute("""SELECT * from list WHERE id = %s """, (str(id)))
    activity = cursor.fetchone()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='activity not found')
    return {'data':activity}

@router.delete('/delete/{id}')
def delete_activity(id:int):
    cursor.execute("""DELETE FROM list WHERE id = %s returning *""",(str(id)))
    deleted_post = cursor.fetchone()
    connect.commit()
    if deleted_post == None : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='post does not exist')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/update/{id}')
def update_activity(id:int,post:Activity):
    cursor.execute("""UPDATE list SET title = %s , description = %s ,time = %s, type = %s,state = %s WHERE id = %s RETURNING *""",(post.title,post.description,post.time,post.type,post.state,str(id)))
    updated = cursor.fetchall()
    connect.commit()
    if updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='activity does not exist')
    return {'message': updated}