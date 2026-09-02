from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"  # for postgres
# SQLALCHEMY_DATABASE_URL = "mysql://user:password@localhost/db_name"  # for mysql


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create base class for declarative models
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    age = Column(Integer)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    def __repre__(self):
        return f"User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, age={self.age})"


# to create tables and database
Base.metadata.create_all(bind=engine)
