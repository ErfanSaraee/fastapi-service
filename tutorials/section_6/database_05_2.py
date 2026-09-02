from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite_05.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# for postgres or other relational databases
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver:5432/db"
# SQLALCHEMY_DATABASE_URL = "mysql://username:password@localhost/db_name"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # only for sqlite
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
    # addresses = relationship("Address")
    # addresses = relationship("Address", back_populates="user")
    addresses = relationship("Address", backref="user")

    def __repr__(self):
        return f"User(id={self.id},username={self.username},email={self.email})"


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    city = Column(String())
    state = Column(String())
    zip_code = Column(String())
    # user = relationship("User")
    # user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id},user_id={self.user_id},city={self.city},state={self.state},zip_code={self.zip_code})"


# to create tables and database
Base.metadata.create_all(bind=engine)

session = SessionLocal()

# session.add(
#     User(
#         username="alibigdeli",
#         email="alibigdeli@gmail.com",
#         password="1234"
#     ))
# session.commit()

user = session.query(User).filter_by(username="alibigdeli").one_or_none()

# addresses = [
#     Address(
#         city="Tehran",
#         state="Tehran",
#         zip_code="34000",
#         user_id=user.id
#     ), Address(
#         city="Mashhad",
#         state="Khorasan-e Razavi",
#         zip_code="35000",
#         user_id=user.id
#     )]
# session.add_all(addresses)
# session.commit()


addresses = session.query(Address).filter_by(user_id=user.id).all()
for address in addresses:
    print(address.user.username)

for address in user.addresses:
    print(address)