from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite_06.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# for postgres or other relational databases
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver:5432/db"
# SQLALCHEMY_DATABASE_URL = "mysql://username:password@localhost/db_name"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # only for sqlite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create base class for declaring tables
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30))
    email = Column(String())
    password = Column(String())
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    addresses = relationship("Address", backref="user")
    profile = relationship("Profile", backref="user", uselist=False)

    def __repr__(self):
        return f"User(id={self.id},username={self.username},email={self.email})"


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    city = Column(String())
    state = Column(String())
    zip_code = Column(String())

    def __repr__(self):
        return f"Address(id={self.id},user_id={self.user_id},city={self.city})"


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    # alternative
    # user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    bio = Column(Text(), nullable=True)

    def __repr__(self):
        return f"Profile(id={self.id},first_name={self.first_name},last_name={self.last_name})"


# to create tables and database
Base.metadata.create_all(engine)

session = SessionLocal()

session.add(
    User(
        username="alibigdeli",
        email="alibigdeli@gmail.com",
        password="1234"
    ))
session.commit()

user = session.query(User).filter_by(username="alibigdeli").one_or_none()

session.add(Profile(first_name="Ali", last_name="Bigdeli", user_id=user.id))
session.commit()

print(user.profile)