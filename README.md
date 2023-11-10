# QuizApp

This is a Python-based console application for a Quiz. The application is designed to manage users, categories, questions, and quizzes. It provides functionality for Super Admins, Admins, and Users. You can use `pipenv` to manage your project dependencies.

## Getting Started

Before running the application, make sure you have created a `.env` file in the project root directory with the following credentials for the Super Admin:

```bash
SUPER_ADMIN_NAME=YourSuperAdminName
SUPER_ADMIN_EMAIL=YourSuperAdminEmail
SUPER_ADMIN_USERNAME=YourSuperAdminUsername
SUPER_ADMIN_PASSWORD=YourSuperAdminPassword
```

### Prerequisites

- Python
- Pipenv
- SQLite database

### Installation

1. Clone this repository:

```bash
https://github.com/Shreyansh-Agrawal/QuizApp.git
```

2. Navigate to the project directory:

```bash
cd QuizApp
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

### Project Structure

```bash
QuizApp/
├── documents/
│   ├── documentation.pdf
├── src/
│   ├── config/
│   │   ├── display_menu.py
│   │   ├── queries.py
│   │   ├── questions.json
│   │   ├── regex_patterns.py
│   ├── controllers/
│   │   ├── handlers/
│   │   │   ├── auth_handler.py
│   │   │   ├── menu_handler.py
│   │   │   ├── quiz_handler.py
│   │   │   ├── user_handler.py
│   │   ├── helpers/
│   │   │   ├── quiz_helper.py
│   │   │   ├── start_quiz_helper.py
│   │   ├── auth_controller.py
│   │   ├── quiz_controller.py
│   │   ├── user_controller.py
│   ├── database/
│   │   ├── data.db
│   │   ├── database_access.py
│   │   ├── database_connection.py
│   ├── models/
│   │   ├── quiz.py
│   │   ├── user.py
│   ├── utils/
│   │   ├── custom_error.py
│   │   ├── initialize_app.py
│   │   ├── json_to_db_loader.py
│   │   ├── menu.py
│   │   ├── pretty_print.py
│   │   ├── validations.py
│   ├── app.py
├── .env
├── .gitignore
├── logs.log
├── Pipfile
├── Pipfile.lock
├── README.md
```

## Models

- **user.py**: Contains classes for users, including `Person`, `SuperAdmin`, `Admin`, and `User`.

- **quiz.py**: Contains classes for quiz entities, such as `QuizEntity`, `Category`, `Option`, and `Question`.

## Controllers

- **auth_controller.py**: Manages user authentication, including signup and login functionalities.

- **quiz_controller.py**: Manages quiz-related operations, including managing categories, questions, and options.

- **user_controller.py**: Manages user-related operations, catering to superadmins, admins, and regular users.

## Database

The application employs an SQLite database with the following tables:

- **Users**: Stores user information.
- **Credentials**: Stores user credentials for authentication.
- **Scores**: Stores user scores.
- **Categories**: Stores quiz categories.
- **Questions**: Stores quiz questions.
- **Options**: Stores options for quiz questions.

## Usage

### Super Admin

- **Create Admin Account**: Super Admins can create new admin accounts.
- **View Admins**: Super Admins can view a list of admins, either all or by specific admin ID.
- **Delete Admin Details**: Super Admins can delete admin accounts.

### Admin

- **Manage Users**: Admins can view user data and delete user accounts.
- **Manage Quizzes**: Admins can add new quiz categories, add questions, and view existing categories and questions.

### User

- **Take a Quiz**: Users can participate in quizzes by selecting a category.
- **View Leaderboard**: Users can see the quiz leaderboard.
- **View Your Scores**: Users can view their own past quiz scores.

Feel free to explore the project, and don't forget to set up your environment and database before running the application.
