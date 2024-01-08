from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
engine = None

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

def setup_session(connection_string):
    global engine 
    engine = create_engine(connection_string)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))

    Base.query = db_session.query_property()

    return db_session

def create_all():
    Base.metadata.create_all(engine)

def drop_all():
    Base.metadata.drop_all(bind=engine)