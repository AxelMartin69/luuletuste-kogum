from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
import models
from datetime import datetime
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

cors_origins = 'http://localhost:3000'

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
