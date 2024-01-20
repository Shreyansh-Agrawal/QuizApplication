# QuizApplication

Welcome to the Quiz Application! This application is designed to manage users, categories, questions, and quizzes. It provides functionality for Super Admins, Admins, and Players. Developed with Python and Flask, the application follows clean code principles, adhering to SOLID principles and object-oriented programming (OOPs) practices. Unit testing is implemented using pytest to ensure robust functionality. This application was created during an internship at WatchGuard, Noida. 

Consider using `pipenv` to manage your project dependencies.

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
JWT_SECRET_KEY=YourSecretKey
SUPER_ADMIN_MAPPING=YourSuperAdminMapping
ADMIN_MAPPING=YourAdminMapping
PLAYER_MAPPING=YourPlayerMapping
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
pipenv run python .\src\server.py
```

### Run the Tests

The application includes unit testing implemented using pytest. To run the Tests, use the following command:

```bash
pipenv shell
pytest
```

### Project Structure

```bash
QuizApplication/
├── docs/
│   ├── API Endpoint Specification.pdf
│   ├── Requirements and Design Specification.pdf
├── src/
│   ├── config/
│   │   ├── file_paths.py
│   │   ├── message_prompts.py
│   │   ├── queries.py
│   │   ├── quiz_data.json
│   │   ├── regex_patterns.py
│   ├── controllers/
│   │   ├── auth.py
│   │   ├── category.py
│   │   ├── question.py
│   │   ├── quiz.py
│   │   ├── user.py
│   ├── database/
│   │   ├── database_access.py
│   │   ├── database_connection.py
│   ├── models/
│   │   ├── database/
│   │   │   ├── category_db.py
│   │   │   ├── database_saver.py
│   │   │   ├── option_db.py
│   │   │   ├── question_db.py
│   │   │   ├── user_db.py
│   │   ├── quiz/
│   │   │   ├── category.py
│   │   │   ├── option.py
│   │   │   ├── question.py
│   │   │   ├── quiz_entity.py
│   │   ├── users/
│   │   │   ├── admin.py
│   │   │   ├── player.py
│   │   │   ├── super_admin.py
│   │   │   ├── user.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── category.py
│   │   ├── question.py
│   │   ├── quiz.py
│   │   ├── user.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── category.py
│   │   ├── question.py
│   │   ├── quiz.py
│   │   ├── user.py
│   ├── utils/
│   │   ├── blocklist.py
│   │   ├── custom_error.py
│   │   ├── error_handlers.py
│   │   ├── initialize_app.py
│   │   ├── password_hasher.py
│   │   ├── rbac.py
│   │   ├── validations.py
│   ├── server.py
├── tests/
│   ├── test_config/
│   │   ├── test_file_paths.py
│   │   ├── test_message_prompts.py
│   │   ├── test_queries.py
│   │   ├── test_questions.json
│   │   ├── test_regex_patterns.py
│   ├── test_controllers/
│   │   ├── test_auth_controller.py
│   │   ├── test_quiz_controller.py
│   │   ├── test_user_controller.py
│   ├── test_database/
│   │   ├── test_database_access.py
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
├── .env.example
├── .gitignore
├── Pipfile
├── Pipfile.lock
├── pytest.ini
├── README.md
```

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

- **Create Admin Account**: Create new admin accounts.
- **View Admins**: View a list of admins.
- **Delete Admin Details**: Delete admin accounts.

### Admin

- **Manage Players**: View player data and delete player accounts.
- **Manage Quizzes**: Add, update, and delete quiz categories and questions. View existing categories and questions.

### Player

- **Take a Quiz**: Participate in quizzes by selecting a category or can play a random quiz.
- **View Leaderboard**: View the quiz leaderboard.
- **View Your Scores**: View their own past quiz scores.

Feel free to explore the project, and don't forget to set up your environment and database before running the application.
