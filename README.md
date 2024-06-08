# GAMESAGE \- CLI Games Lookup App

![GameSage image](lib/assets/gamesage.jpg)

Welcome to my first Python CLI App! <br>

This project uses Python, SQLAlchemy, and external libraries such as Tabulate, PyFiglet and Colorama.

## What's it About?

This CLI Games Lookup enables users to log in or sign up - view games, manage favourite games and notes associated with them.

## Getting Started

1. Clone the Repository:

```bash
git clone https://github.com/emilychewsh/phase-3-games-db-cli-project.git
cd phase-3-games-db-cli-project
```

2. Install the dependencies:

```bash
pipenv install
```

3. Set up the virtual environment using Pipenv.

```bash
pipenv shell
```

4. Happy browsing!

## Usage

Upon running the application, users will be prompted to either log in or sign up. From the main menu, users can choose to view all games, view their favorite list, or exit the app. Users can look up games, add them to their favorites, make notes, and manage their notes all through a user-friendly CLI.

## Database Schema

These are the 3 main tables used with SQLAlchemy to establish many to many relationships:

### User

| Column | Type    | Description          |
| ------ | ------- | -------------------- |
| id     | Integer | Primary key          |
| name   | String  | User names to log in |

### Game

| Column      | Type    | Description        |
| ----------- | ------- | ------------------ |
| id          | Integer | Primary key        |
| title       | String  | Title of game      |
| genre       | String  | Genre of game      |
| price       | Integer | Price of game      |
| description | String  | Storyline of game  |
| rating      | Intger  | Game rating        |
| platform    | String  | Platform available |
| trailer     | String  | Youtube URL        |

### Favaourite

| Column  | Type    | Description             |
| ------- | ------- | ----------------------- |
| id      | Integer | Primary key             |
| note    | String  | Notes of favourite      |
| user_id | Integer | Foreign Key for `users` |
| game_id | Integer | Foreign Key for `games` |

## Credits:

- [Colorama](https://pypi.org/project/colorama/) for colours used.
- [Tabulate](https://pypi.org/project/tabulate/) for tables used.
- [PyFiglet](https://pypi.org/project/pyfiglet/) for title used.

## License

This project is licensed under the MIT License.

## Contribution Guidelines

If you would like to contribute to the project development:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and submit a pull request.

Feel free to adjust any details or formatting to better suit your project and preferences!

## Contact

For any inquiries or feedback, please contact codewithemilychew@gmail.com.
