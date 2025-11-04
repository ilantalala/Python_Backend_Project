from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from typing import Optional,List
import time
from .. import models,schemas,oauth2
from sqlalchemy.orm import Session
from .. database import get_db
from sqlalchemy import func

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)
              ,limit:int=10,skip:int=0,search:Optional[str]=""):

    posts=db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()
    results=db.query(models.Post,func.count(models.Vote.post_id)).join(models.Vote,
                                                                       models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).all()
 
    print(f'results: {results}')
    rows = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes"),
        )
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
        .filter(models.Post.content.contains(search))
        .group_by(models.Post.id)
        .limit(limit)
        .offset(skip)
        .all()
    )
    return [schemas.PostOut(Post=post, votes=votes) for post, votes in rows]
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    print(f'id:{current_user.id}')
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
@router.get("/{id}")
def get_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {id} was not found')
    
    return post
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    deleted_post=db.query(models.Post).filter(models.Post.id==id)
    if deleted_post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with this id does not exist.')
    if deleted_post.first().owner_id!=current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requested action')
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
@router.put("/{id}")
def update_post(id:int,new_post:schemas.PostBase,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==id)
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with this id does not exist.')
    if post.first().owner_id!=current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requested action')
    post.update(new_post.dict(),synchronize_session=False)
    db.commit()
    return post.first()