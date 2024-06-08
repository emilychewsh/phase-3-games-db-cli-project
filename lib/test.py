from config import session
from models import Game, User, Favourite

if __name__ == "__main__":
    
    # Delete all favourites
    session.query(Favourite).delete()
    
    # Delete all users
    session.query(User).delete()
    
    session.commit()
    
    print("All users, favourites, and notes have been deleted.")   