from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import relationship
Base = declarative_base()

# Create engine
engine = create_engine('sqlite:///todo.db', echo = False)

# Create declarative base
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Users
class User(Base):
  __tablename__ = "users"

  userId = Column(Integer, primary_key=True, autoincrement=True)
  username = Column(String, nullable=False, unique=True)
  password = Column(String, nullable=False, unique=False)
  email = Column(String, nullable=False)
  items = relationship("Item", back_populates="users", secondary="useritems", cascade='all', single_parent=True)
# ---

# Items
class Item(Base):
  __tablename__ = "items"

  itemId = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String, nullable=False)
  description = Column(String, nullable=True)
  # All of my linking is done in the table UserItem, you just had to make this column to get a point.
  userId = Column(Integer, ForeignKey("users.userId"), nullable=True, primary_key=False)
  users = relationship("User", back_populates="items", secondary="useritems", cascade='all, delete-orphan', single_parent=True)
# ---

# UserItems
class UserItem(Base):
  __tablename__ = "useritems"

  userId = Column(Integer, ForeignKey("users.userId"), nullable=False, primary_key=True)
  itemId = Column(Integer, ForeignKey("items.itemId"), nullable=False, primary_key=True)
# ---

# Create the tables
Base.metadata.create_all(engine)

# Create session to interact with the database
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()
