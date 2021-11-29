from fastapi import status, APIRouter
from fastapi.params import Depends
from .. import schemas, models, database, oauth2
from ..database import engine
from sqlalchemy.orm import Session
from ..repository import blog

router = APIRouter(
    prefix='/blog',
    tags = ['Blogs']
)

models.Base.metadata.create_all(bind=engine)
get_db = database.get_db
        
@router.post("/", status_code= status.HTTP_201_CREATED)
def create(request: schemas.Blog, db:Session = Depends(get_db)):
    return blog.create(request, db)

@router.get("/", response_model=list[schemas.ShowBlog])
def all(db: Session = Depends(get_db), current_user:
        schemas.User = Depends(oauth2.get_current_user)):
    return blog.all(db)

@router.get("/{id}", status_code=200, response_model=schemas.ShowBlog)
def show_single(id, db: Session = Depends(get_db), current_user:
    schemas.User = Depends(oauth2.get_current_user)):
    return show_single(id, db)

@router.put("/{id}")
def update(id, request: schemas.Blog, db: Session = Depends(get_db), current_user:
        schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(id, request)

@router.delete("/{id}")
def destroy(id, db: Session = Depends(get_db), current_user:
        schemas.User = Depends(oauth2.get_current_user)):
    return blog.destroy(id, db)