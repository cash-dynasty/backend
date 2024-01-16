import models.user
import schemas.user
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.auth import get_password_hash


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


# 1. User utworzony poprawnie
# 2. Email niepoprawny
# 3. User z takim emailem już istnieje
# 4. Hasło za krótkie/długie, brak wymaganych znaków (obecnie tego nie sprawdzamy)
@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.user.UserOut)
async def create_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    user_data = db.query(models.user.User).filter(models.user.User.email == user.email).first()
    if user_data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    new_user = models.user.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# 1. email i token zgodny - user aktywowany
# 2. niepoprawny email
# 3. nie ma takiego maila w bazie
# 4. niepoprawny token dla danego usera
@router.patch("/activate")
async def activate_user(user: schemas.user.UserActivation, db: Session = Depends(get_db)):
    user = db.query(models.user.User).filter(models.user.User.email == user.email).first()
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user  # TODO nie zwracać wszystkich danych usera


# TODO zrobić endpoint do generowania nowego tokena aktywacyjnego
