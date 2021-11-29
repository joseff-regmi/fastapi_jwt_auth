from fastapi import status, HTTPException
from fastapi.params import Depends
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session

def create(request: schemas.Blog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def all(db: Session = Depends(get_db)):
    all_blogs = db.query(models.Blog).all()
    return all_blogs

def show_single(id, db: Session = Depends(get_db)):
    _blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not _blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail = f"blog with the id {id} not found")
    return _blog

def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog =db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail = f"blog with the id {id} not found")
    blog.update(request.dict())
    db.commit()
    return "updated sucessfully"


def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id) 
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail = f"blog with the id {id} not found") 
    blog.delete(synchronize_session=False)
    db.commit()
    return "done"