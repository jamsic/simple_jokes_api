import os
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'users'
    id_ = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(120), nullable=False)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def serialize(self):
        return {
            'id': self.id_,
            'username': self.username
        }


class JokeModel(Base):
    __tablename__ = 'jokes'
    id_ = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id_'))
    text = Column(String(120), nullable=False, unique=True)

    def __repr__(self):
        return '<Joke %r>' % self.text

    @property
    def serialize(self):
        return {
            'id': self.id_,
            'user_id': self.user_id,
            'text': self.text
        }

basedir = os.path.abspath(os.path.dirname(__file__))
database_path = 'sqlite:///' + os.path.join(basedir, 'jokes.db')
engine = create_engine(database_path)
Base.metadata.create_all(engine)
Base.metadata.bind = engine
session = scoped_session(sessionmaker(bind=engine))

