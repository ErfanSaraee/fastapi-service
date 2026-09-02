from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Text,
    DateTime,
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, backref

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite_07.db"
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
    posts = relationship("Post", backref="user")
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
    first_name = Column(String())
    last_name = Column(String())
    bio = Column(Text(), nullable=True)

    def __repr__(self):
        return f"Profile(id={self.id},first_name={self.first_name},last_name={self.last_name})"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String())
    content = Column(Text())

    comments = relationship("Comment", backref="post")

    created_date = Column(DateTime(), default=datetime.now)
    updated_date = Column(
        DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"Post(id={self.id},title={self.title})"


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)

    # parent = relationship("Comment", remote_side=[
    #                       id], back_populates="children")
    # children = relationship("Comment", remote_side=[
    #                         parent_id], back_populates="parent")
    children = relationship("Comment", backref=backref("parent", remote_side=[id]))
    

    content = Column(Text())
    created_date = Column(DateTime(), default=datetime.now)

    def __repr__(self):
        return f"Comment(id={self.id},post_id={self.post_id},user_id={self.user_id},parent_id={self.parent_id},content={self.content})"


# to create tables and database
Base.metadata.create_all(engine)

session = SessionLocal()

# session.add(
#     User(
#         username="alibigdeli",
#         email="alibigdeli@gmail.com",
#         password="1234"
#     ))
# session.commit()

user = session.query(User).filter_by(username="alibigdeli").one_or_none()

# session.add(Post(user_id=user.id, title="post 1", content="content 1"))
# session.commit()

post = user.posts[0]

# session.add(Comment(user_id=user.id, post_id=post.id, content="comment 1"))
# session.commit()

parent_comment = post.comments[0]

# session.add(Comment(user_id=user.id, post_id=post.id,
#             parent_id=parent_comment.id, content="comment 2 (reply of comment 1)"))
# session.commit()


# session.add(Comment(user_id=user.id, post_id=post.id,
#             parent_id=parent_comment.id, content="comment 3 (reply of comment 1)"))
# session.commit()

comments = session.query(Comment).filter_by(
    post_id=post.id, parent_id=None).all()

for comment in comments:
    print(comment.children)