'''Contains all the messages and prompts displayed to user'''

from collections import namedtuple

INFO = namedtuple('StatusCodes', 'code status')


class Message:
    '''Contains all the print messages as class variables'''

    APP_WELCOME = '---------WELCOME TO QUIZ APP---------'
    EXIT = '---------END OF APP---------'
    AUTH_INVALIDATE = 'Invalid Credentials! Please Try Again or Sign Up...'
    CONFIRM_PSWD_FAIL = 'Password does not match. Please re-enter your password!'
    LOGIN_SUCCESS = 'Successfully Logged In!'
    SIGNUP_SUCCESS = 'Account created successfully!'
    DISPLAY_QUES_IN_A_CATEGORY = '-----Questions in {name}-----'
    CREATE_CATEGORY = '-----Create a new Quiz Category-----'
    CREATE_CATEGORY_SUCCESS = 'Category Created'
    CREATE_QUES = '-----Create a new Quiz Question-----'
    CREATE_QUES_SUCCESS = 'Question Created!'
    INVALID_QUES_TYPE = 'Invalid Question Type! Please choose from above!!'
    UPDATE_CATEGORY = '-----Update a Category-----'
    UPDATE_CATEGORY_SUCCESS = 'Category updated successfully'
    DELETE_CATEGORY = '-----Delete a Category-----'
    DELETE_CATEGORY_WARNING = 'WARNING: All the questions in {name} will be deleted as well'
    DELETE_CATEGORY_SUCCESS = 'Category deleted successfully'
    DISPLAY_SCORE = 'You Scored: {score}'
    TF_OPTION = '   1. True   2. False'
    MCQ_WRONG_OPTION = 'Please enter a number from 1 to 4 ... '
    TF_WRONG_OPTION = 'Please enter either 1 or 2...'
    CREATE_ADMIN = '-----Create a new Admin-----'
    CREATE_ADMIN_SUCCESS = 'Admin created successfully!'
    DELETE_USER = '-----Delete a {user}-----'
    DELETE_USER_FAIL = 'No such {user}! Please choose from above!!'
    DELETE_USER_SUCCESS = '{user}: {email} deleted successfully!'
    LOGIN = '----Login----'
    REMAINING_ATTEMPTS = 'Remaining attempts: {count}'
    LOGIN_ATTEMPTS_EXHAUST = 'Account Not Found! Please Sign up!'
    SIGNUP = '----SignUp----'
    REDIRECT = 'Redirecting...'
    CHANGE_PSWD = 'Please change your password...'
    CHANGE_PSWD_SUCCESS = 'Password changed successfully!'
    WRONG_INPUT = 'Wrong input! Please choose from the above given options...'
    LOAD_QUES = 'Questions Added!'
    MANAGE_CATEGORIES = '----Manage Categories----'
    MANAGE_QUES = '----Manage Questions----'
    CATEGORIES = '-----Quiz Categories-----'
    QUES_NOT_FOUND = 'No Questions Currently, Please add a question!!'
    QUES = '-----Quiz Questions-----'
    QUIZ_DATA_NOT_FOUND = 'No data! Take a Quiz...'
    LEADERBOARD = '-----Leaderboard-----'
    QUIZ_START = '-----Quiz Starting-----'
    REVIEW_RESPONSES = '-----REVIEW YOUR RESPONSES-----'
    CATEGORY_NOT_FOUND = 'No such Category! Please choose from above!!'
    USER_NOT_FOUND = 'No {user} Currently!'
    DISPLAY_USERS = '-----List of {user}s-----'
    SCORE_DATA = '-----Score History-----'
    HIGHEST_SCORE = 'Highest Score: {score}'
    CREATE_SUPER_ADMIN_SUCCESS = 'Super Admin created!'
    INITIALIZATION_SUCCESS = 'Initialization Complete!'
    USER_WELCOME = '----Welcome {user}----'
    MANAGE_PLAYERS = '----Manage Players----'
    MANAGE_QUIZ = '----Manage Quizzes----'
    DASHBOARD = '----{user} Dashboard----'
    INVALID_ROLE = 'Invalid Role!: '
    TABULATE_ERROR = 'Could not pretty print...'
    TRY_AGAIN = '{error} Please try again...'
    INVALID_TEXT = 'Invalid {}'
    INVALID_CHOICE = 'Select a number from above options!'
    INVALID_PASSWORD = 'Invalid password! Length cannot be less than 6!'
    CONFIRMATION = 'Type "YES" if you wish to continuePress any other key to go back: '
    SELECT_QUIZ = '-----SELECT QUIZ MODE-----'
    SUCCESS = 'Request successful'
    LOGOUT_SUCCESS = 'Logged out successfully'
    ADMIN_CREATED = 'Admin created successfully'
    PLAYER_CREATED = 'Player created successfully'
    QUESTION_CREATED = 'Question created successfully'
    QUIZ_POSTED = 'Quiz data posted successfully'
    ADMIN_DELETED = 'Admin deleted successfully'
    PLAYER_DELETED = 'Player deleted successfully'
    QUESTION_DELETED = 'Question deleted successfully'
    QUESTION_UPDATED = 'Question updated successfully'
    PROFILE_UPDATED = 'Profile updated successfully'
    PASSWORD_UPDATED = 'Password updated successfully'
    SUBMISSION_SUCCESS = 'Response submitted successfully'


class Headers:
    '''Contains all the headings as class variables'''

    USERNAME = 'Username'
    NAME = 'Name'
    EMAIL = 'Email'
    PASSWORD = 'Password'
    REG_DATE = 'Registration Date'
    CATEGORY = 'Category'
    CATEGORIES = 'Categories'
    QUES = 'Question'
    QUES_TYPE = 'Question Type'
    ANS = 'Correct Answer'
    CREATED_BY = 'Created By'
    SCORE = 'Score'
    TIME = 'Time'
    ID = 'ID'
    OPTION = 'Option'
    PLAYER_ANS = 'Your Answer'
    SUPER_ADMIN = 'Super Admin'
    ADMIN = 'Admin'
    PLAYER = 'Player'
    QUIZZES = 'Quizzes'
    PROFILE = 'Profile'


class LogMessage:
    '''Contains all the log messages as class variables'''

    LOGIN_INITIATED = 'Login Initiated'
    LOGIN_SUCCESS = 'Login Successful'
    LOGOUT_INITIATED = 'Logout Initiated'
    LOGOUT_SUCCESS = 'Logout Successful, Token added to blocklist'
    SIGNUP_INITIATED = 'Signup Initiated'
    SIGNUP_SUCCESS = 'Signup Successful'
    SYSTEM_START = 'System Started'
    SYSTEM_STOP = 'Stopping Application'
    INITIALIZE_APP_SUCCESS = 'Initialization Complete'
    CREATE_ENTITY = 'Creating %s'
    CREATE_SUCCESS = '%s Created'
    UPDATE_ENTITY = 'Updating %s'
    UPDATE_SUCCESS = '%s Updated'
    DELETE_ENTITY = 'Deleting %s'
    DELETE_SUCCESS = '%s Deleted'
    DELETE_CATEGORY = 'Deleting Category %s'
    DELETE_CATEGORY_SUCCESS = 'Category %s deleted'
    CHANGE_DEFAULT_ADMIN_PSW = 'Changing Default Admin Password'
    CHANGE_DEFAULT_ADMIN_PSW_SUCCESS = 'Default Admin Password Changed'
    UPDATE_CATEGORY_SUCCESS = 'Category %s updated to %s'
    GET_QUES_BY_CATEGORY = 'Get Questions by Category'
    START_QUIZ = 'Starting Quiz for: %s'
    COMPLETE_QUIZ = 'Quiz Completed for: %s'
    RUNNING_USER_MENU = 'Running %s Menu'
    RUNNING_AUTH_MENU = 'Running auth_menu'
    ASSIGN_MENU = 'Assigning menu according to the role'
    SUPER_ADMIN_PRESENT = 'Super Admin Present'
    TABULATE_ERROR = 'Tabulate error: %s'
    SAVE_QUIZ_SCORE = 'Saving score for: %s'
    SAVE_QUIZ_SCORE_SUCCESS = 'Score saved for: %s'
    DISPLAY_QUIZ_SCORE = 'Display score for: %s'
    DISPLAY_ALL_ENTITY = 'Display all %s'
    DISPLAY_QUES_BY_CATEGORY = 'Display Questions By Category'
    INVALID_QUES_TYPE = 'Invalid Ques Type!'
    LOGIN_ATTEMPTS_EXHAUSTED = 'Login attempts exhausted'
    GET_LEADERBOARD = 'Fetching leaderboard data'
    LEADERBOARD_DATA_NOT_FOUND = 'No Data in Leaderboard'
    QUES_DATA_NOT_FOUND = 'No Questions added'
    RUNNING_ADMIN_MENU = 'Running Admin: Manage %s Menu'
    LOAD_QUIZ_DATA_FROM_JSON = 'Loading Quiz Data from JSON'
    GET_ALL_CATEGORIES = 'Fetching all categories'
    TOKEN_CREATED = 'Access token created'
    REFRESH_INITIATED = 'Creating a non fresh access token'
    GET_QUIZ_DATA = 'Fetching the quiz data'
    POST_QUIZ_DATA = 'Posting quiz data'
    GET_PROFILE_DATA = 'Getting profile data'
    GET_PROFILE_DATA = 'Getting profile data'
    GET_ALL_USERS = 'Getting all users with role: %s'
    EVALUATE_RESPONSE = 'Evaluating answers for player_id: %s'
    GET_QUES_FOR_QUIZ = 'Fetching questions for quiz'
    GET_SCORES = 'Fetching scores for player_id: %s'


class ErrorMessage:
    '''Contains all the error messages as class variables'''

    USER_EXISTS = 'User already exists'
    INVALID_CREDENTIALS = 'Invalid credentials'
    ENTITY_EXISTS = '{entity} already exists!'
    CATEGORY_EXISTS = 'Category already exists!'
    QUESTION_EXISTS = 'Question already exists!'
    INSUFFICIENT_QUESTIONS = 'Not enough questions!'
    INVALID_CATEGORY_SELECTION = 'No such Category! Please choose from above!!'
    NO_CATEGORY = 'No Category Added!'
    NO_ROLE = 'No {role} Currently!'
    NO_OPTIONS = 'No Options added for this Question!'
    CATEGORY_NOT_FOUND = 'Category does not exists'
    USER_NOT_FOUND = 'User does not exists'
    EMAIL_TAKEN = 'This email is not available'
    USERNAME_TAKEN = 'This username is not available'
    LEADERBOARD_NOT_FOUND = 'No data in the leaderboard'
    SCORES_NOT_FOUND = 'No scores for this player'
    QUESTIONS_NOT_FOUND = 'No questions present'
    QUESTION_NOT_FOUND = 'Question not found'
    QUIZ_NOT_FOUND = 'Quiz data not found'
    TOKEN_REVOKED = 'The token has been revoked'
    TOKEN_NOT_FRESH = 'The token is not fresh'
    TOKEN_EXPIRED = 'The token has expired'
    INVALID_TOKEN = 'Signature verification failed'
    MISSING_TOKEN = 'Request does not contain an access token'
    SERVER_ERROR = 'Something went wrong'
    BAD_REQUEST = 'Invalid request syntax'
    FORBIDDEN = 'Access denied'


class Roles:
    '''Contains all the user roles'''

    SUPER_ADMIN = 'super_admin'
    ADMIN = 'admin'
    PLAYER = 'player'


class StatusCodes:
    'Contains all the status codes and messages'

    OK = INFO(code=200, status='Ok')
    CREATED = INFO(code=201, status='Created')
    BAD_REQUEST = INFO(code=400, status='Bad Request')
    UNAUTHORIZED = INFO(code=401, status='Unauthorized')
    FORBIDDEN = INFO(code=403, status='Forbidden')
    NOT_FOUND = INFO(code=404, status='Not Found')
    CONFLICT = INFO(code=409, status='Conflict')
    UNPROCESSABLE_ENTITY = INFO(code=422, status='Unprocessable Entity')
    INTERNAL_SERVER_ERROR = INFO(code=500, status='Internal Server Error')


QUESTION_TYPES = ['mcq', 't/f', 'one word', 'MCQ', 'T/F', 'ONE WORD']


AUTHORIZATION_HEADER = {
    "name": "Authorization",
    "in": "header",
    "description": "Bearer <access_token>",
    "required": "true",
}
