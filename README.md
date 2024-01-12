# QuizApplication

This is a Python-based console application for Quiz management. The application is designed to manage users, categories, questions, and quizzes. It provides functionality for Super Admins, Admins, and Players. You can use `pipenv` to manage your project dependencies.

## Getting Started

Before running the application, make sure you have created a `.env` file in the project root directory with the following credentials for the Super Admin:

```bash
SUPER_ADMIN_NAME=YourSuperAdminName
SUPER_ADMIN_EMAIL=YourSuperAdminEmail
SUPER_ADMIN_USERNAME=YourSuperAdminUsername
SUPER_ADMIN_PASSWORD=YourSuperAdminPassword
MYSQL_USER=YourMySQLusername
MYSQL_PASSWORD=YourMySQLpassword
MYSQL_HOST=YourMySQLhost
MYSQL_DB=YourMySQLdb
```

### Prerequisites

- Python
- Pipenv
- MySQL database

### Installation

1. Clone this repository:

```bash
https://github.com/Shreyansh-Agrawal/QuizApplication.git
```

2. Navigate to the project directory:

```bash
cd QuizApplication
```

3. Install project dependencies using pipenv:
   
```bash
pipenv install
```
or
```bash
python -m pipenv install
```

### Run the Application

To run the application, use the following command:

```bash
pipenv run python .\src\app.py
```

### Run the Tests

To run the Tests, use the following command:

```bash
pipenv shell
pytest
```

### Project Structure

```bash
QuizApplication/
├── docs/
│   ├── documentation.pdf
├── src/
│   ├── config/
│   │   ├── file_paths.py
│   │   ├── message_prompts.py
│   │   ├── queries.py
│   │   ├── questions.json
│   │   ├── regex_patterns.py
│   ├── controllers/
│   │   ├── auth.py
│   │   ├── category.py
│   │   ├── question.py
│   │   ├── quiz.py
│   │   ├── user.py
│   ├── helpers/
│   │   ├── auth_handler.py
│   │   ├── create_quiz_helper.py
│   │   ├── quiz_handler.py
│   │   ├── start_quiz_helper.py
│   │   ├── user_handler.py
│   ├── menu/
│   │   ├── admin_menu.py
│   │   ├── main_menu.py
│   │   ├── player_menu.py
│   │   ├── super_admin_menu.py
│   ├── models/
│   │   ├── database/
│   │   │   ├── database_access.py
│   │   │   ├── database_saver.py
│   │   ├── quiz/
│   │   │   ├── category.py
│   │   │   ├── option.py
│   │   │   ├── question.py
│   │   │   ├── quiz_entity.py
│   │   ├── users/
│   │   │   ├── admin.py
│   │   │   ├── player.py
│   │   │   ├── super_admin.py
│   │   │   ├── user_manager.py
│   │   │   ├── user.py
│   ├── utils/
│   │   ├── custom_error.py
│   │   ├── initialize_app.py
│   │   ├── json_to_db_loader.py
│   │   ├── password_hasher.py
│   │   ├── pretty_print.py
│   │   ├── validations.py
│   ├── app.py
├── tests/
│   ├── test_config/
│   │   ├── test_file_paths.py
│   │   ├── test_message_prompts.py
│   │   ├── test_queries.py
│   │   ├── test_questions.json
│   │   ├── test_regex_patterns.py
│   ├── test_controllers/
│   │   ├── test_handlers/
│   │   │   ├── test_auth_handler.py
│   │   │   ├── test_quiz_handler.py
│   │   │   ├── test_user_handler.py
│   │   ├── test_helpers/
│   │   │   ├── test_create_quiz_helper.py
│   │   │   ├── test_start_quiz_helper.py
│   │   ├── test_auth_controller.py
│   │   ├── test_quiz_controller.py
│   │   ├── test_user_controller.py
│   ├── test_database/
│   │   ├── test_database_access.py
│   ├── test_menu/
│   │   ├── test_admin_menu.py
│   │   ├── test_main_menu.py
│   │   ├── test_player_menu.py
│   │   ├── test_super_admin_menu.py
│   ├── test_models/
│   │   ├── test_database_saver.py
│   │   ├── test_quiz.py
│   │   ├── test_user_manager.py
│   │   ├── test_user.py
│   ├── test_utils/
│   │   ├── test_custom_error.py
│   │   ├── test_initialize_app.py
│   │   ├── test_json_to_db_loader.py
│   │   ├── test_pretty_print.py
│   │   ├── test_password_hasher.py
│   │   ├── test_validations.py
│   ├── conftest.py
│   ├── test_app.py
├── .env
├── .gitignore
├── logs.log
├── Pipfile
├── Pipfile.lock
├── pytest.ini
├── README.md
```

## Models

- **user.py**: Contains classes for users, including `User`, `SuperAdmin`, `Admin`, and `Player`.

- **quiz.py**: Contains classes for quiz entities, such as `QuizEntity`, `Category`, `Option`, and `Question`.

- **database_saver.py**: Contains interface for `DatabaseSaver`.

- **user_manager.py**: Contains classes responsible for saving users to the database, such as `UserManager`.

## Controllers

- **auth_controller.py**: Manages user authentication, including signup and login functionalities.

- **quiz_controller.py**: Manages quiz-related operations, including managing categories, questions, and options.

- **user_controller.py**: Manages user-related operations, catering to superadmins, admins, and players.

## Database

The application employs an MySQL database with the following tables:

- **Users**: Stores user information.
- **Credentials**: Stores user credentials for authentication.
- **Scores**: Stores player scores.
- **Categories**: Stores quiz categories.
- **Questions**: Stores quiz questions.
- **Options**: Stores options for quiz questions.

## Usage

### Super Admin

- **Create Admin Account**: Super Admins can create new admin accounts.
- **View Admins**: Super Admins can view a list of admins.
- **Delete Admin Details**: Super Admins can delete admin accounts.

### Admin

- **Manage Players**: Admins can view player data and delete player accounts.
- **Manage Quizzes**: Admins can add new quiz categories, add questions, and view existing categories and questions.

### Player

- **Take a Quiz**: Players can participate in quizzes by selecting a category or can play a random quiz.
- **View Leaderboard**: Players can see the quiz leaderboard.
- **View Your Scores**: Players can view their own past quiz scores.

Feel free to explore the project, and don't forget to set up your environment and database before running the application.
