from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, database, tokens
from ..hashing import Hash
from datetime import datetime, timedelta


router = APIRouter(
    tags=['Authentication']
)

get_db = database.get_db

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid credentials")
        
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid password or username")
        
    #generate jwt (json web tokens) and return it
    access_token_expires = timedelta(minutes=tokens.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = tokens.create_access_token(
                    data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}