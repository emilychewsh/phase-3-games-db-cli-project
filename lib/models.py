from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.associationproxy import association_proxy


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)

    favourites = relationship("Favourite", back_populates="user")
    games = association_proxy("favourites", "game", creator= lambda g: Favourite(game=g))

    def __repr__(self):
        return f"{self.id}: {self.name}"
    
class Game(Base):
    __tablename__ = "games"

    id = Column(Integer(), primary_key=True)
    title = Column(String(), nullable=False)
    genre = Column(String(), nullable=False)
    price = Column(Integer(), nullable=False)
    description = Column(String(), nullable=False)
    rating = Column(Integer(), nullable=False)
    platform = Column(String(), nullable=False)
    trailer = Column(String(), nullable=False)

    favourites = relationship("Favourite", back_populates="game")
    users = association_proxy("favourites", "user", creator= lambda u: Favourite(user=u))

    def __repr__(self):
        return f"{self.id} - {self.title} | {self.genre}"

class Favourite(Base):
    __tablename__ = "favourites"

    id = Column(Integer(), primary_key=True)

    user_id = Column(Integer(), ForeignKey("users.id"))
    game_id = Column(Integer(), ForeignKey("games.id"))
    note = Column(String())
    note_date_time = Column(DateTime, nullable=False) 

    user = relationship("User", back_populates="favourites")
    game = relationship("Game", back_populates="favourites")

    def __repr__(self):
        return f"{self.user.name} favourited the game called '{self.game.title}' "
