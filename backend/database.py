from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('mysql://root:password@localhost:3306/JournalAppDb')
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = 'User'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Password = Column(String(255), nullable=False)
    Name = Column(String(255), nullable=False)

class JournalEntry(Base):
    __tablename__ = 'JournalEntry'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Date = Column(Date, nullable=False)
    Content = Column(Text, nullable=False)

class UserJournalEntry(Base):
    __tablename__ = 'UserJournalEntry'
    UserId = Column(Integer, ForeignKey('User.Id'), primary_key=True)
    JournalEntryId = Column(Integer, ForeignKey('JournalEntry.Id'), primary_key=True)
    
    user = relationship("User")
    journal_entry = relationship("JournalEntry")

def init_db():
    metadata.create_all(bind=engine)

def add_user(username, password):
    new_user = User(Name=username, Password=password)
    db_session.add(new_user)
    db_session.commit()
    return True

def user_exists(username):
    user = db_session.query(User).filter_by(Name=username).first()
    return user is not None

def user_with_password_exists(username, password):
    user = db_session.query(User).filter_by(Name=username, Password=password).first()
    return user is not None