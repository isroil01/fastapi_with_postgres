from fastapi import APIRouter,status,HTTPException,Response,Depends
from config.database import get_db
from sqlalchemy.orm import Session
from model.list import Activities,Activity
from oauth import get_current_user


router  = APIRouter(prefix='',tags=['Activity'])

# new
@router.get('/activities')
def get_all (db:Session = Depends(get_db)):
    activity = db.query(Activities).all()
    return {'data':activity}

@router.post('/create',status_code=status.HTTP_201_CREATED)
def create_activity (post:Activity,db:Session = Depends(get_db),current_user:int =Depends(get_current_user)):
    data = Activities(**post.dict())
    db.add(data)
    db.commit()
    db.refresh(data)
    return {'data': data}

@router.get('/activity/{id}')
def get_by_id(id:int,db :Session = Depends(get_db)):
    activity = db.query(Activities).filter(Activities.id == id).first()
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='for the gien id activity not found')
    return { 'data':activity}

@router.delete('/delete/{id}')
def delete_item(id:int,db:Session = Depends(get_db)):
    activity = db.query(Activities).filter(Activities.id == id)
    if activity.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='not found')
    activity.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/update/{id}')
def update_activity(id:int,post:Activity,db:Session=Depends(get_db)):
    act_query = db.query(Activities).filter(Activities.id == id)
    act = act_query.first()
    if act == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='activity not found for the given id')
    act_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return {'message': act_query.first()}