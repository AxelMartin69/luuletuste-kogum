from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from datetime import datetime, timedelta


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "d04dc20b5a85b7a54e1cf9061a82afd12515cb2007e8ba0a1908e35f46e604aa"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class Poem(BaseModel):
    title: str
    body: str


models.Base.metadata.create_all(bind=engine)

cors_origins = 'http://localhost:3000'

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_populate_db():
    db = SessionLocal()
    num_poems = db.query(models.Poem).count()
    num_users = db.query(models.User).count()
    num_likes = db.query(models.likes).count()
    if num_poems == 0:
        poems = [
            {
                'title': 'Advent',
                'body': 'Milline rahu on südames, advendiaeg on süüdi ses. See on nii hea ja magus süü, jõuludel aeg tulla on nüüd.',
                'entry_time': datetime.now(),
                'owner_id': 1
            },
            {
                'title': 'Jõulud',
                'body': 'Jõulud tulevad tasa, tasa, tasa langeb lumigi. Jõulud tulevad rahus, rahus, jõuavad kõikide hingeni.',
                'entry_time': datetime.now(),
                'owner_id': 2
            }
        ]
        for poem in poems:
            db.add(models.Poem(**poem))
        db.commit()
    else:
        print(f'Poems table has {num_poems} entries')
    if num_users == 0:
        users = [
            {
                "username": "johndoe",
                "full_name": "John Doe",
                "email": "johndoe@example.com",
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                "is_active": True,
            },
            {
                "username": "alice",
                "full_name": "Alice Smith",
                "email": "alice@example.com",
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                "is_active": True,
            }
        ]
        for user in users:
            db.add(models.User(**user))
        db.commit()
    else:
        print(f'Users table has {num_users} entries')
    if num_likes == 0:
        likes = [
            {
                'poem_id': 1,
                'user_id': 2
            }
        ]
        for like in likes:
            db.execute(models.likes.insert().values(**like))
        db.commit()
    else:
        print(f'Likes table has {num_likes} entries')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60*24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def validate_token(token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exception


# Get all poems
@app.get('/')
async def get_poems(db: Session = Depends(get_db)):
    poems = db.query(models.Poem).all()
    for i in range(len(poems)):
        # count likes where poem_id = poem.id
        poems[i].likes = db.execute(
            f'SELECT COUNT(poem_id) FROM likes WHERE poem_id = {poems[i].id}').fetchall()[0][0]
        # get username where user_id = poem.owner_id
        poems[i].author = db.execute(
            f'SELECT username FROM users WHERE id = {poems[i].owner_id}').fetchall()[0][0]
    return poems

# Get token


@ app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # get user from db by username
    user = db.query(models.User).filter(
        models.User.username == form_data.username).first()

    # authenticate user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Create new poem
@app.post('/poems/new')
def create_new_poem(poem: Poem, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_data = validate_token(token)

    try:
        title = poem.title
        body = poem.body
        owner_id = db.execute('SELECT id FROM users WHERE username = :username', {
            'username': token_data.username}).fetchall()[0][0]
        db.execute('INSERT INTO poems (title, body, owner_id) VALUES (:title, :body, :owner_id)', {
            'title': title, 'body': body, 'owner_id': owner_id})
        db.commit()
        return {'message': 'Poem created successfully'}
    except:
        return {'message': 'Something went wrong'}
