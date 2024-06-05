from config import session
from models import User, Game, Favourite
from colorama import Back, Fore, Style
import os

logged_user = None

def clear(): #Clearing terminal
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")


def login(username): #Check if user exists
    user = session.query(User).filter(User.name == username).first()

    if not user:
        user = User(name=username)
        session.add(user)
        session.commit()

        print(f"Hi {user.name}, you have successfully been registered into the Crux Games App!")

    else:
        clear()
        print(f"Welcome back, {user.name}")

    global logged_user
    logged_user = user


def greet(): #Greet
    print("Welcome to Crux games database where you can look up your favourite games!")
    print("Please enter your username to log in or sign up by entering a username:")
    
    username = input()
    login(username)


def main_menu():
    print(f"-"*30)
    print("By Emily Chew")
    print(f"-"*30)

    print("Please select where you want to go...")
    print("1. " + "View all games")
    print("2. " + "View your saved favourites")
    print("3. " + "Exit this app")

    choice = input()
    return choice #Return user's choice


##################################################### Functions for choices 

def save_to_favourites(game): #Save game to favourites, but also checks it is already in list
    existing_favourite = session.query(Favourite).filter_by(user_id=logged_user.id, game_id=game.id).first()
    if existing_favourite:
        print(f"'{game.title}' is already in your favourites.")
    else:
        favourite = Favourite(user_id=logged_user.id, game_id=game.id)
        session.add(favourite)
        session.commit()
        print(f"You have successfully saved the game '{game.title}' to your favourite list!")


def view_all_games():
    games = session.query(Game).all()
    if len(games)>0:
        for game in games:
            print(game)
    else:
        print("No games...")
    
    print('-'*30)
    print("\nPlease enter the game ID to view more details (type 'back' to go back):")

    id_input = input()

    if id_input == "back":
        clear()
        return
    else:
        try:
            game_id = int(id_input)
            game = [ g for g in games if g.id == game_id ]

            if len(game)>0:
                game = game[0]
                
                clear()

                #Print and display game info for selected ID
                print(f"{game.title.upper()}")
                print(f"GENRE: {game.genre}")
                print(f"DESCRIPTION: {game.description}")

                print("Other Details")
                print(f"Rating: {game.rating}")
                print(f"Platform: {game.platform}")
                print(f"Trailer: {game.trailer}")

                #Ask to see if user wants to save game to favourites
                print("Would you like add this game to your favourite list? (yes/no)")
                save_input = input().lower()
                if save_input == "yes":
                    save_to_favourites(game)
                elif save_input == "no":
                    return
                else:
                    print("Please enter a valid input: 'yes/no")

            else:
                print("No game found! Try again.")
        
        except ValueError:
            print("Invalid input. Please enter a valid game ID or 'back' to return to previous selection.")
           
def add_note_to_favourite(game_id):
        favourite = session.query(Favourite).filter_by(user_id=logged_user.id, game_id=game_id).first()
        if favourite:
            note = input("Enter your note:")
            favourite.note = note
            session.commit()
            print(f"Your note is successfully added to '{favourite.game.title}'!")
        else:
            print("Favourite game not found")

def view_favourites():
    while True:
        favourites = session.query(Favourite).filter_by(user_id=logged_user.id).all()
        if len(favourites)>0:
            for fav in favourites:
                game = fav.game
                note = fav.note if fav.note else "No notes added."
                print(f"{game.id}) {game.title} - {game.genre}")
        else:
            print("You have no favourite games yet.")

        print("\nPlease choose from the following options:")
        print("1) View details of a favourite game")
        print("2) View all games in general")
        print("3) Return to main menu")

        choice = input().lower()

        if choice == "1":
            try:
                game_id = int(input("Enter Game ID:"))
                favourite = session.query(Favourite).filter_by(user_id=logged_user.id, game_id=game_id).first()
                if favourite:
                    game = favourite.game
                    clear()
                    print(f"{game.title.upper()}")
                    print(f"GENRE: {game.genre}")
                    print(f"DESCRIPTION: {game.description}")

                    print("Other Details")
                    print(f"Rating: {game.rating}")
                    print(f"Platform: {game.platform}")
                    print(f"Trailer: {game.trailer}")

                    print("-"*30)
                    print("MY OWN NOTES")
                    print("-"*30)
                    print(f"{favourite.note if favourite.note else 'No notes added yet.'}")
                    
                    #Ask user if they want to add a note to this game 
                    subchoice = input("Do you want to add a note to this game? (yes/no):").lower()
                    if subchoice == "yes":
                        add_note_to_favourite(game_id)
                    elif subchoice == "no":
                        continue

                else:
                    print("No game found with that ID")
            except ValueError:
                print("Invalid input. Please enter a valid game ID.")

        elif choice == "2":
            clear()
            view_all_games()

        elif choice == "3":
            clear()
            break
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")




#####################################################
def start():
    greet()

    while True:
        choice = main_menu()
        if choice == "1":
            clear()
            view_all_games()
            # print("Do you want to view games in general or by genre?")
        elif choice == "2":
            clear()
            view_favourites()
        elif choice == "3":
            clear()
            print("Thank you for using Crux Games App, see you again!")
            break
        else:
            print("Please enter a valid selection")
            choice = main_menu()


#############################################################

if __name__ == "__main__":
    start()