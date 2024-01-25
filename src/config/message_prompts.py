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
    CONFIRMATION='Type "YES" if you wish to continuePress any other key to go back: '
    SELECT_QUIZ='-----SELECT QUIZ MODE-----'
    SUCCESS='Request successful'
    LOGOUT_SUCCESS='Logged out successfully'
    ADMIN_CREATED='Admin created successfully'
    PLAYER_CREATED='Player created successfully'
    QUESTION_CREATED='Question created successfully'
    QUIZ_POSTED='Quiz data posted successfully'
    ADMIN_DELETED='Admin deleted successfully'
    PLAYER_DELETED='Player deleted successfully'
    QUESTION_DELETED='Question deleted successfully'
    QUESTION_UPDATED='Question updated successfully'
    PROFILE_UPDATED='User data updated successfully'
    SUBMISSION_SUCCESS='Response submitted successfully'


class Prompts:
    '''Contains all the prompts as class variables'''

    AUTH_PROMPTS = '''
Enter -
        1> Login
        2> Signup
        
        Press q to Quit

Enter your choice: '''

    SUPER_ADMIN_PROMPTS = '''
Enter -
        1> Create Admin
        2> View All Admins
        3> Delete Admin
        
        Press q to Logout

Enter your choice: '''

    ADMIN_PROMPTS = '''
Enter -
        1> Manage Players
        2> Manage Quizzes
        
        Press q to Logout

Enter your choice: '''

    ADMIN_MANAGE_PLAYER_PROMPTS = '''
Enter -
        1> View All Players
        2> Delete a Player

        Press q to Go Back

Enter your choice: '''

    ADMIN_MANAGE_QUIZZES_PROMPTS = '''
Enter -
        1> Manage Categories
        2> Manage Questions
        
        Press q to Go Back

Enter your choice: '''

    ADMIN_MANAGE_CATEGORIES_PROMPTS = '''
Enter -
        1> View All Categories
        2> Add a New Category
        3> Update a Category
        4> Delete a Category
        
        Press q to Go Back

Enter your choice: '''

    ADMIN_MANAGE_QUESTIONS_PROMPTS = '''
Enter -
        1> View All Questions
        2> View Questions By Category
        3> Add a Question
        4> Load Questions from JSON File
        
        Press q to Go Back

Enter your choice: '''

    PLAYER_PROMPTS = '''
Enter -
        1> Take a Quiz
        2> View Leaderboard
        3> View Scores History
        
        Press q to Logout

Enter your choice: '''


    QUESTION_TYPE_PROMPTS = '''
Enter -
        1> Multiple Choice Question Type
        2> True or False Type
        3> One Word Type

Select Question Type: '''


    SELECT_MODE_PROMPTS = '''
Enter -
        1> Simple (Choose a Category)
        2> Random (Questions Across All Categories)

        Press q to Go Back

Select Mode: '''

    USERNAME_PROMPT='Enter your username: '
    CREATE_USERNAME_PROMPT='Create your username: '
    PASSWORD_PROMPT='Enter your password: '
    CREATE_PASSWORD_PROMPT='Create your password: '
    CONFIRM_PASSWORD_PROMPT='Confirm Password: '
    NEW_PASSWORD_PROMPT='Enter New Password: '
    NAME_PROMPT='Enter your name: '
    EMAIL_PROMPT='Enter your email: '
    SELECT_CATEGORY_PROMPT='Choose a Category: '
    NEW_CATEGORY_NAME_PROMPT='Enter New Category Name: '
    UPDATED_CATEGORY_NAME_PROMPT='Enter updated category name: '
    ADMIN_NAME_PROMPT='Enter admin name: '
    ADMIN_EMAIL_PROMPT='Enter admin email: '
    ADMIN_USERNAME_PROMPT='Create admin username: '
    USER_EMAIL_PROMPT='Enter {role} Email: '
    QUES_TEXT_PROMPT='Enter Question Text: '
    ANS_PROMPT='Enter Answer: '
    OPTION_PROMPT='Enter Other Option: '
    SELECT_OPTION_PROMPT='Choose an option: '
    ANS_INPUT_PROMPT='-> Enter your answer: '
    ATTEMPT_LIMIT = 3


class Headers:
    '''Contains all the headings as class variables'''

    USERNAME='Username'
    NAME='Name'
    EMAIL='Email'
    PASSWORD='Password'
    REG_DATE='Registration Date'
    CATEGORY='Category'
    CATEGORIES='Categories'
    QUES='Question'
    QUES_TYPE='Question Type'
    ANS='Correct Answer'
    CREATED_BY='Created By'
    SCORE='Score'
    TIME='Time'
    ID='ID'
    OPTION='Option'
    PLAYER_ANS='Your Answer'
    SUPER_ADMIN='Super Admin'
    ADMIN='Admin'
    PLAYER='Player'
    QUIZZES='Quizzes'


class LogMessage:
    '''Contains all the log messages as class variables'''

    LOGIN_INITIATED='Login Initiated'
    LOGIN_SUCCESS='Login Successful'
    SIGNUP_INITIATED='Signup Initiated'
    SIGNUP_SUCCESS='Signup Successful'
    SYSTEM_START='System Started'
    SYSTEM_STOP='Stopping Application'
    INITIALIZE_APP_SUCCESS='Initialization Complete'
    CREATE_ENTITY='Creating %s'
    CREATE_SUCCESS='%s Created'
    UPDATE_ENTITY='Updating %s'
    UPDATE_SUCCESS='%s Updated'
    DELETE_ENTITY='Deleting %s'
    DELETE_SUCCESS='%s Deleted'
    DELETE_CATEGORY='Deleting Category %s'
    DELETE_CATEGORY_SUCCESS='Category %s deleted'
    CHANGE_DEFAULT_ADMIN_PSW='Changing Default Admin Password'
    CHANGE_DEFAULT_ADMIN_PSW_SUCCESS='Default Admin Password Changed'
    UPDATE_CATEGORY_SUCCESS='Category %s updated to %s'
    GET_QUES_BY_CATEGORY='Get Questions by Category'
    START_QUIZ='Starting Quiz for: %s'
    COMPLETE_QUIZ='Quiz Completed for: %s'
    RUNNING_USER_MENU='Running %s Menu'
    RUNNING_AUTH_MENU='Running auth_menu'
    ASSIGN_MENU='Assigning menu according to the role'
    SUPER_ADMIN_PRESENT='Super Admin Present'
    TABULATE_ERROR='Tabulate error: %s'
    SAVE_QUIZ_SCORE='Saving score for: %s'
    SAVE_QUIZ_SCORE_SUCCESS='Score saved for: %s'
    DISPLAY_QUIZ_SCORE='Display score for: %s'
    DISPLAY_ALL_ENTITY='Display all %s'
    DISPLAY_QUES_BY_CATEGORY='Display Questions By Category'
    INVALID_QUES_TYPE='Invalid Ques Type!'
    LOGIN_ATTEMPTS_EXHAUSTED='Login attempts exhausted'
    LEADERBOARD_DATA_NOT_FOUND='No Data in Leaderboard'
    QUES_DATA_NOT_FOUND='No Questions added'
    RUNNING_ADMIN_MENU='Running Admin: Manage %s Menu'
    LOAD_QUIZ_DATA_FROM_JSON='Loading Quiz Data from JSON'
    GET_ALL_CATEGORIES='Fetching all categories'


class ErrorMessage:
    '''Contains all the error messages as class variables'''

    USER_EXISTS='User already exists'
    INVALID_CREDENTIALS='Invalid credentials'
    ENTITY_EXISTS='{entity} already exists!'
    CATEGORY_EXISTS='Category already exists!'
    QUESTION_EXISTS='Question already exists!'
    INSUFFICIENT_QUESTIONS='Not enough questions!'
    INVALID_CATEGORY_SELECTION='No such Category! Please choose from above!!'
    NO_CATEGORY='No Category Added!'
    NO_ROLE='No {role} Currently!'
    NO_OPTIONS='No Options added for this Question!'
    CATEGORY_NOT_FOUND='Category does not exists'
    USER_NOT_FOUND='User does not exists'
    EMAIL_TAKEN='This email is not available'
    USERNAME_TAKEN='This username is not available'
    LEADERBOARD_NOT_FOUND='No data in the leaderboard'
    SCORES_NOT_FOUND='No scores for this player'
    QUESTIONS_NOT_FOUND='No questions present'
    QUESTION_NOT_FOUND='Question not found'
    QUIZ_NOT_FOUND='Quiz data not found'


class Roles:
    '''Contains all the user roles'''

    SUPER_ADMIN='super_admin'
    ADMIN='admin'
    PLAYER='player'


class StatusCodes:
    'Contains all the status codes and messages'

    OK =INFO(code=200, status='OK')
    CREATED=INFO(code=201, status='CREATED')
    BAD_REQUEST=INFO(code=400, status='BAD REQUEST')
    UNAUTHORIZED=INFO(code=401, status='UNAUTHORIZED')
    FORBIDDEN=INFO(code=403, status='FORBIDDEN')
    NOT_FOUND=INFO(code=404, status='NOT FOUND')
    CONFLICT=INFO(code=409, status='CONFLICT')
    UNPROCESSABLE_CONTENT=INFO(code=422, status='UNPROCESSABLE CONTENT')
    INTERNAL_SERVER_ERROR=INFO(code=500, status='INTERNAL SERVER ERROR')
