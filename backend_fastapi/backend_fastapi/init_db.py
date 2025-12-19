from models import Base
from database import engine, SessionLocal
import crud

def init():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not crud.get_user_by_email(db, 'admin@local'):
        crud.create_user(db, 'admin@local', 'admin123', 'Admin Local')
    db.close()

if __name__ == '__main__':
    init()
    print('DB initialized and admin user seeded (admin@local / admin123)')
