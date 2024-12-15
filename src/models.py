from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

# Tabla Follower (relación muchos a muchos entre usuarios)
class Follower(Base):
    __tablename__ = 'followers'
    user_from_id = Column(Integer, ForeignKey('users.id'), primary_key=True) # foreign se conecta al id de users
    user_to_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    user_from = relationship('User', foreign_keys=[user_from_id], backref='following')
    user_to = relationship('User', foreign_keys=[user_to_id], backref='followers')

# Tabla User (información del usuario)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    firstname = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(100), unique=True)

    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='author')

# Tabla Post (cada post pertenece a un usuario)
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='posts')
    media = relationship('Media', back_populates='post')
    comments = relationship('Comment', back_populates='post')

# Tabla Media (relación uno a muchos con Post)
class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String(50))
    url = Column(String(250))
    post_id = Column(Integer, ForeignKey('posts.id'))

    post = relationship('Post', back_populates='media')

# Tabla Comment (relación uno a muchos con Post y uno a muchos con User)
class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, nullable=False)
    comment_text = Column(Text)
    author_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')


# Rendering
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
