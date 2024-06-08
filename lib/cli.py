from config import session
from models import User, Game, Favourite
from colorama import Back, Fore, Style
from datetime import datetime
import pyfiglet 
from tabulate import tabulate
import os

logged_user = None

def clear(): #Clearing terminal
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")


def login(username): #Check if user exists
    global logged_user
    user = session.query(User).filter(User.name == username).first()

    if not user:
        clear()
        user = User(name=username)
        session.add(user)
        session.commit()

        print(f"Hi {user.name}, you have successfully been registered into the Crux Games App!")

    else:
        clear()
        print(f"Welcome back,{Fore.LIGHTGREEN_EX} {user.name} {Style.RESET_ALL}!")

    logged_user = user


def greet(): #Greet
    clear()
    styled_title = pyfiglet.figlet_format("WELCOME TO CRUX GAMES LOOKUP!", font="small")
    print(Fore.LIGHTGREEN_EX + styled_title + Style.RESET_ALL)
    print("\nWelcome to Crux games database where you can look up your favourite games!")
    print("\nPlease enter your username to log in or sign up by entering a username: ")
    
    username = input(Fore.LIGHTGREEN_EX)
    print(Style.RESET_ALL, end="")
    login(username)


def main_menu():
    print(f"-"*65)
    print(Fore.LIGHTBLUE_EX + "Crux Games Lookup By Emily Chew | e: codewithemilychew@gmail.com" + Style.RESET_ALL)
    print(f"-"*65)

    print(Fore.LIGHTGREEN_EX + "\n1) " + Style.RESET_ALL + "\tView all games")
    print(Fore.LIGHTGREEN_EX + "2) " + Style.RESET_ALL + "\tView your saved favourites")
    print(Fore.LIGHTGREEN_EX + "3) " + Style.RESET_ALL + "\tExit this app")

    print("\nPlease select where you want to go...")
    choice = input(Fore.LIGHTGREEN_EX).lower()
    print(Style.RESET_ALL, end="")
    return choice #Return user's choice

##################################################### Functions for choices 

def save_to_favourites(game): #Save game to favourites, but also checks it is already in list
    existing_favourite = session.query(Favourite).filter_by(user_id=logged_user.id, game_id=game.id).first()
    if existing_favourite:
        print(Fore.LIGHTGREEN_EX + game.title + Style.RESET_ALL + " is already in your favourites.")
    else:
        favourite = Favourite(user_id=logged_user.id, game_id=game.id)
        session.add(favourite)
        session.commit()
        print("You have successfully saved the game " + Fore.LIGHTGREEN_EX + game.title + Style.RESET_ALL + " to your favourite list!")

def delete_from_favourites(game_id):
    favourite = session.query(Favourite).filter_by(user_id=logged_user.id, game_id=game_id).first()
    if favourite:
        clear()
        session.delete(favourite)
        session.commit()
        print(Fore.LIGHTGREEN_EX + favourite.game.title + Style.RESET_ALL + " was removed from favourites.\n")
    else:
        print(Fore.LIGHTRED_EX + "No favourite game found with that ID." + Style.RESET_ALL)


def print_heading(heading):
    print("-"*50)
    print(heading)
    print("-"*50)

def view_game_details(game, from_favourites=False):
    clear()
    
    # Bold the game title
    title = game.title.upper()
    centered_title = '\033[1m' + title + '\033[0m'
    print_heading(Back.LIGHTGREEN_EX + centered_title + Style.RESET_ALL)

    print("\nGenre: " + Fore.LIGHTGREEN_EX + game.genre + Style.RESET_ALL)
    print("\nRating: " + Fore.LIGHTGREEN_EX + str(game.rating) + Style.RESET_ALL + "\n")
          
    print_heading("Description")
    print(Fore.LIGHTGREEN_EX + game.description + Style.RESET_ALL + "\n")

    print_heading("Other details")
    print("Platform: " + Fore.LIGHTGREEN_EX + game.platform + Style.RESET_ALL)
    print("\nTrailer URL: " + Fore.LIGHTGREEN_EX + game.trailer + Style.RESET_ALL)
    #Shows the number of people who has this game in their favourite list 
    favourite_count = session.query(Favourite).filter_by(game_id=game.id).count()
    print("\nNumber of users who have favourited this game: " + Fore.LIGHTMAGENTA_EX + str(favourite_count) + Style.RESET_ALL)

    if not from_favourites:
        #Ask to see if user wants to save game to favourites
        print("\nWould you like add this game to your favourite list? (yes/no)")
        save_input = input(Fore.LIGHTGREEN_EX).lower()
        print(Style.RESET_ALL, end="")
        if save_input == "yes":
            clear()
            save_to_favourites(game)
        elif save_input == "no":
            clear()
            return
        else:
            print(Fore.LIGHTRED_EX + "\nPlease enter a valid input: 'yes/no'" + Style.RESET_ALL)
    else:
        print_heading("MY OWN NOTES")
        favourite = session.query(Favourite).filter_by(user_id=logged_user.id, game_id=game.id).first()
        if favourite and favourite.note:
            print(Fore.LIGHTGREEN_EX + favourite.note + Style.RESET_ALL)
        else:
            print(Fore.LIGHTRED_EX + "No notes added yet." + Style.RESET_ALL)
                    
        # Ask user if they want to add a note to this game 
        subchoice = input("\nDo you want to add a note to this game? (yes/no): ").lower()
        if subchoice == "yes":
            clear()
            add_note_to_favourite(game.id)
        elif subchoice == "no":
            clear()
            return


def view_by_genre():
    genres = ["RPG", "Action", "Anime", "Battle", "Racing"]

    print("\nGenres: \n") #Display the genre in a numbered list
    for idx, genre in enumerate(genres, 1):
        print(Fore.LIGHTGREEN_EX + str(idx) + ")" +  "\t" + Style.RESET_ALL + genre)
    
    print("\nEnter the genre number you want to view(or type 'back' to return): \n")
    genre_choice = input(Fore.LIGHTGREEN_EX)
    print(Style.RESET_ALL, end="")
    if genre_choice.lower() == "back":
        clear()
        return

    #Validate and process genre selection
    try:
        genre_idx = int(genre_choice) - 1
        if 0<= genre_idx < len(genres):
            selected_genre = genres[genre_idx]
            games = session.query(Game).filter_by(genre=selected_genre).all()

            #Display games in selected genre
            if games:
                table = []
                for game in games:
                    table.append([game.id, game.title, game.genre, game.rating])
                
                headers = [Fore.LIGHTGREEN_EX + "Game ID" + Fore.RESET, Fore.LIGHTBLUE_EX + "Title" + Fore.RESET, Fore.LIGHTMAGENTA_EX + "Genre" + Fore.RESET, Fore.LIGHTRED_EX + "Rating" + Fore.RESET]
                print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


                print("\nPlease enter the game ID to view more details (type 'back' to return): ")
                id_input = input(Fore.LIGHTGREEN_EX)
                print(Style.RESET_ALL, end="")
                if id_input == "back":
                    clear()
                    return
                else:
                    try:
                        game_id = int(id_input)
                        game = session.query(Game).filter_by(id=game_id, genre=selected_genre).first()

                        #Display game detals or handle invalid input
                        if game:
                            view_game_details(game)
                        else:
                            print(Fore.LIGHTRED_EX + "\nNo game found with that ID in the selected genre." + Style.RESET_ALL)
                    except ValueError:
                        print(Fore.LIGHTRED_EX + "\nInvalid input.Please enter valid game ID or 'back' to return to previous selection" + Style.RESET_ALL)
            
            else:
                print(Fore.LIGHTRED_EX + "\nNo games found in this genre." + Style.RESET_ALL)
        else:
            print(Fore.LIGHTRED_EX + "Invalid genre selection." + Style.RESET_ALL)
            return
    except ValueError:
        print(Fore.LIGHTRED_EX + "Invalid input. Please enter a valid genre number or 'back' to return." + Style.RESET_ALL)

                    

def view_all_games():
    while True:
        print("\nHow would you like to view the games?\n")
        print(Fore.LIGHTGREEN_EX + "1) " + Style.RESET_ALL + "\tView games in general")
        print(Fore.LIGHTGREEN_EX + "2) " + Style.RESET_ALL + "\tView games by genre")
        print(Fore.LIGHTGREEN_EX + "3) " + Style.RESET_ALL + "\tReturn to main menu")

        print("\nEnter your choice: ", end="")
        choice = input(Fore.LIGHTGREEN_EX + Style.BRIGHT).lower()
        print(Style.RESET_ALL, end="")

        if choice == "1":
            clear()
            games = session.query(Game).all()
            if len(games)>0:
                table = []
                for game in games:
                    table.append([game.id, game.title, game.genre, game.rating])
                
                headers = [
                    Fore.LIGHTGREEN_EX + "Game ID" + Fore.RESET, 
                    Fore.LIGHTBLUE_EX + "Title" + Fore.RESET, 
                    Fore.LIGHTMAGENTA_EX + "Genre" + Fore.RESET, 
                    Fore.LIGHTRED_EX + "Rating" + Fore.RESET
                    ]
                print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
            else:
                print("No games...")
            

            #Entering Game ID to view more details about a game
            print("\nPlease enter the game ID to view more details (type 'back' to go back):")
            id_input = input(Fore.LIGHTGREEN_EX)
            print(Style.RESET_ALL, end="")
            if id_input == "back":
                clear()
                return
            else:
                try:
                    game_id = int(id_input)
                    game = session.query(Game).filter_by(id=game_id).first()

                    if game:
                        view_game_details(game)
                    else:
                        print(Fore.LIGHTRED_EX + "\nNo game found! Try again." + Style.RESET_ALL)
                        return
                
                except ValueError:
                    print(Fore.LIGHTRED_EX + "\nInvalid input. Please enter a valid game ID or 'back' to return to previous selection." + Style.RESET_ALL)

        elif choice == "2":
            clear()
            view_by_genre()
        elif choice == "3":
            clear()
            return
        else:
            print(Fore.LIGHTRED_EX + "\nInvalid choice. Please enter 1, 2, or 3." + Style.RESET_ALL)

           
def add_note_to_favourite(game_id):
        favourite = session.query(Favourite).filter_by(user_id=logged_user.id, game_id=game_id).first()
        if favourite:
            print("Enter your note: ")
            note = input(Fore.LIGHTGREEN_EX)
            print(Style.RESET_ALL, end="")
            favourite.note = note
            session.commit()
            print("\nYour note is successfully added to " + Fore.LIGHTGREEN_EX + favourite.game.title + Style.RESET_ALL + "!")
        else:
            print("Favourite game not found")

def delete_note_from_favourite(game_id):
    favourite = session.query(Favourite).filter_by(user_id=logged_user.id, game_id=game_id).first()
    if favourite: 
        favourite.note = None #Clear the note
        session.commit()
    else:
        print("Favourite game not found")

    
def view_notes():
    while True:
        favourites_with_notes = session.query(Favourite).filter(Favourite.user_id == logged_user.id, Favourite.note.isnot(None)).all()
        if favourites_with_notes:
            print("Your Notes:")
            table = []
            for fav in favourites_with_notes:
                table.append([fav.game.id, fav.game.title, fav.game.genre, fav.note])
                
            headers = [
                Fore.LIGHTGREEN_EX + "Game ID" + Fore.RESET, 
                Fore.LIGHTBLUE_EX + "Title" + Fore.RESET, 
                Fore.LIGHTMAGENTA_EX + "Genre" + Fore.RESET, 
                Fore.LIGHTRED_EX + "Note" + Fore.RESET
                ]
            print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
        else:
            print("You have no notes for any of your favourite games.")
        
        print("\nPlease choose from the following options:")
        print(Fore.LIGHTGREEN_EX + "1) " + Style.RESET_ALL + "\tDelete a note")
        print(Fore.LIGHTGREEN_EX + "2) " + Style.RESET_ALL + "\tReturn to previous page")

        choice = input(Fore.LIGHTGREEN_EX).lower()
        print(Style.RESET_ALL, end="")

        if choice == "1":
            try:
                print("Enter Game ID of the note to delete: ")
                game_id = int(input(Fore.LIGHTGREEN_EX))
                print(Style.RESET_ALL, end="")
                favourite = session.query(Favourite).filter_by(user_id=logged_user.id, game_id=game_id).first()
                if favourite:
                    clear()
                    delete_note_from_favourite(game_id)
                    print("Successfully deleted note from " + Fore.LIGHTGREEN_EX + fav.game.title + Style.RESET_ALL + "!")
            except ValueError:
                print(Fore.LIGHTRED_EX + "\nInvalid input. Please enter a valid Game ID." + Style.RESET_ALL)
        
        elif choice == "2":
            clear()
            return
        
        else:
            print(Fore.LIGHTRED_EX + "\nInvalid choice. Please enter 1 or 2." + Style.RESET_ALL)


def view_favourites():
    while True:
        favourites = session.query(Favourite).filter_by(user_id=logged_user.id).all()
        if len(favourites)>0:
            table = []
            for fav in favourites:
                game = fav.game
                note = fav.note if fav.note else "No notes added."
                table.append([game.id, game.title, game.genre, game.rating])
                
            headers = [
                Fore.LIGHTGREEN_EX + "Game ID" + Fore.RESET, 
                Fore.LIGHTBLUE_EX + "Title" + Fore.RESET, 
                Fore.LIGHTMAGENTA_EX + "Genre" + Fore.RESET, 
                Fore.LIGHTRED_EX + "Rating" + Fore.RESET
                ]
            print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
        else:
            print("\nYou have no favourite games yet. Please add some to your favourite list.")

        print("\nPlease choose from the following options:\n")
        print(Fore.LIGHTGREEN_EX + "1) " + Style.RESET_ALL + "\tView details of a favourite game")
        print(Fore.LIGHTGREEN_EX + "2) " + Style.RESET_ALL + "\tDelete a game from favourite list")
        print(Fore.LIGHTGREEN_EX + "3) " + Style.RESET_ALL + "\tGames Lookup")
        print(Fore.LIGHTGREEN_EX + "4) " + Style.RESET_ALL + "\tView all notes")
        print(Fore.LIGHTGREEN_EX + "5) " + Style.RESET_ALL + "\tReturn to main menu")

        choice = input(Fore.LIGHTGREEN_EX).lower()
        print(Style.RESET_ALL, end="")
        if choice == "1":
            try:
                print("Enter Game ID: ")
                game_id = int(input(Fore.LIGHTGREEN_EX))
                print(Style.RESET_ALL, end="")
                favourite = session.query(Favourite).filter_by(user_id=logged_user.id, game_id=game_id).first()
                if favourite:
                    game = favourite.game
                    clear()
                    view_game_details(game, from_favourites=True)
                else:
                    print("No game found with that ID")
            except ValueError:
                print(Fore.LIGHTRED_EX + "\nInvalid input. Please enter a valid game ID." + Style.RESET_ALL)

        elif choice == "2":
            try: 
                print("Enter Game ID to delete from favourites: ")
                game_id = int(input(Fore.LIGHTGREEN_EX))
                print(Style.RESET_ALL, end="")
                delete_from_favourites(game_id)
            except ValueError:
                print(Fore.LIGHTRED_EX + "\nInvalid input. Please enter a valid game ID." + Style.RESET_ALL)


        elif choice == "3":
            clear()
            view_all_games()

        elif choice == "4":
            clear()
            view_notes()
        elif choice == "5":
            clear()
            break
        else:
            print(Fore.LIGHTRED_EX + "\nInvalid choice. Please enter 1, 2, 3, 4 or 5." + Style.RESET_ALL)




#####################################################
def start():
    greet()

    while True:
        choice = main_menu()
        if choice == "1":
            clear()
            view_all_games()
        elif choice == "2":
            clear()
            view_favourites()
        elif choice == "3":
            clear()
            print(f"Thank you for using Crux Games App, see you again soon {Fore.GREEN}{logged_user.name}{Style.RESET_ALL}!")
            break
        else:
            print(Fore.LIGHTRED_EX + "\nInvalid choice. Please enter 1, 2, or 3." + Style.RESET_ALL)
            choice = main_menu()
            

#############################################################

if __name__ == "__main__":
    start()