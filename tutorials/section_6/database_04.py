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
    last_name = Column(String(30), nullable=True)
    age = Column(Integer)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    def __repr__(self):
        return f"User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, age={self.age})"


# to create tables and database
Base.metadata.create_all(bind=engine)


session = SessionLocal()

# inserting data
# ali = User(
#     first_name="Ali",
#     age=30
# )

# session.add(ali)
# session.commit()


# bulk insert
# hasti = User(
#     first_name="Hasti",
#     age=30
# )
# shayna = User(
#     first_name="Shayna",
#     age=19
# )

# session.add_all([hasti, shayna])
# session.commit()


# retrieving all data
# users = session.query(User).all()

# for user in users:
#     print(user)


# retrieving specific data with filter_by
# users = session.query(User).filter_by(first_name="Ali", age=30).all()  # .all() -> .first() or .one_or_none()

# for user in users:
#     print(user)


# updating a record of data
# user = session.query(User).filter_by(first_name="Ali", age=30).first()

# user.last_name = "Rezaei"
# session.commit()


# deleting a record of data
user = session.query(User).filter_by(first_name="Hasti", age=30).first()
if user:
    session.delete(user)
    session.commit()