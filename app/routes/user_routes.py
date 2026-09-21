from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    """Fetch all seeded users for dynamic selection."""
    users = db.query(models.User).all()
    return users

@router.post("/bulk", response_model=List[schemas.UserResponse])
def create_users_bulk(payload: schemas.UserBulkCreate, db: Session = Depends(get_db)):
    """Dynamically create users."""
    created_users = []
    for name in payload.names:
        dummy_email = f"{uuid.uuid4().hex[:8]}@temp.com"
        db_user = models.User(name=name, email=dummy_email)
        db.add(db_user)
        created_users.append(db_user)
    db.commit()
    for user in created_users:
        db.refresh(user)
    return created_users
