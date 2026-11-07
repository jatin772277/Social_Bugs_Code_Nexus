from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from app.core.config import get_settings

settings=get_settings()
db_url=settings.database_url
connect_args={"check_same_thread":False} if db_url.startswith("sqlite") else {}
engine_kwargs={"pool_pre_ping":True} if not db_url.startswith("sqlite") else {}
engine=create_engine(db_url,connect_args=connect_args,**engine_kwargs)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
