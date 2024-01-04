from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import time

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
    JoinPoint = Column(BigInteger, nullable=False)

class JournalEntry(Base):
    __tablename__ = 'JournalEntry'
    UserId = Column(Integer, ForeignKey('User.Id'), primary_key=True)
    Year = Column(Integer, primary_key=True)
    Month = Column(Integer, primary_key=True)
    Day = Column(Integer, primary_key=True)
    LastModified = Column(BigInteger, nullable=False)
    Content = Column(Text, nullable=False)

    user = relationship("User")

Base.metadata.create_all(engine)

def add_user(username, password):
    epoch_time = int(time.time())
    new_user = User(Name=username, Password=password,JoinPoint=epoch_time)
    db_session.add(new_user)
    db_session.commit()
    return True

def get_user_id(username, password):
    user = db_session.query(User).filter_by(Name=username,Password=password).first()
    return user.Id

def user_exists(username):
    user = db_session.query(User).filter_by(Name=username).first()
    return user is not None

def user_with_password_exists(username, password):
    user = db_session.query(User).filter_by(Name=username, Password=password).first()
    return user is not None

def get_journal_entry(year, month, day, user_id):
    entry = db_session.query(JournalEntry).filter_by(Year=year,Month=month,Day=day,UserId=user_id).first()
    return entry

def add_journal_entry(new_entry):
    db_session.add(new_entry)
    db_session.commit()
