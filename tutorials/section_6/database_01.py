from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"  # for postgres
# SQLALCHEMY_DATABASE_URL = "mysql://user:password@localhost/db_name"  # for mysql


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create base class for declarative models
Base = declarative_base()


# to create tables and database
Base.metadata.create_all(bind=engine)