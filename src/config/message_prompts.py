'''Contains all the messages and prompts displayed to user'''


class DisplayMessage:
    '''Contains all the print messages as class variables'''

    APP_WELCOME_MSG = '\n---------WELCOME TO QUIZ APP---------\n'
    EXIT_MSG = '\n---------END OF APP---------\n'
    AUTH_INVALIDATE_MSG = '\nInvalid Credentials! Please Try Again or Sign Up...'
    CONFIRM_PSWD_FAIL_MSG = '\nPassword does not match. Please re-enter your password!\n'
    LOGIN_SUCCESS_MSG = '\nSuccessfully Logged In!\n'
    SIGNUP_SUCCESS_MSG = '\nAccount created successfully!\n'
    DISPLAY_QUES_IN_A_CATEGORY_MSG = '\n-----Questions in {name}-----\n'
    CREATE_CATEGORY_MSG = '\n-----Create a new Quiz Category-----\n'
    CREATE_CATEGORY_SUCCESS_MSG = '\nCategory Created!\n'
    CREATE_QUES_MSG = '\n-----Create a new Quiz Question-----\n'
    CREATE_QUES_SUCCESS_MSG = '\nQuestion Created!\n'
    INVALID_QUES_TYPE_MSG = 'Invalid Question Type! Please choose from above!!'
    UPDATE_CATEGORY_MSG = '\n-----Update a Category-----\n'
    UPDATE_CATEGORY_SUCCESS_MSG = '\nCategory: {name} updated to {new_name}!\n'
    DELETE_CATEGORY_MSG = '\n-----Delete a Category-----\n'
    DELETE_CATEGORY_WARNING_MSG = '\nWARNING: All the questions in {name} will be deleted as well'
    DELETE_CATEGORY_SUCCESS_MSG = '\nCategory: {name} deleted!\n'
    DISPLAY_SCORE_MSG = '\nYou Scored: {score}'
    TF_OPTION_MSG = '   1. True\n   2. False'
    MCQ_WRONG_OPTION_MSG = 'Please enter a number from 1 to 4 ... '
    TF_WRONG_OPTION_MSG = 'Please enter either 1 or 2...'
    CREATE_ADMIN_MSG = '\n-----Create a new Admin-----\n'
    CREATE_ADMIN_SUCCESS_MSG = '\nAdmin created successfully!\n'
    DELETE_USER_MSG = '\n-----Delete a {user}-----\n'
    DELETE_USER_FAIL_MSG = 'No such {user}! Please choose from above!!'
    DELETE_USER_SUCCESS_MSG = '\n{user}: {email} deleted successfully!\n'
    LOGIN_MSG = '\n----Login----\n'
    REMAINING_ATTEMPTS_MSG = 'Remaining attempts: {count}\n'
    LOGIN_ATTEMPTS_EXHAUST_MSG = 'Account Not Found! Please Sign up!'
    SIGNUP_MSG = '\n----SignUp----\n'
    REDIRECT_MSG = 'Redirecting...'
    CHANGE_PSWD_MSG = '\nPlease change your password...\n'
    CHANGE_PSWD_SUCCESS_MSG = '\nPassword changed successfully!\n'
    WRONG_INPUT_MSG = 'Wrong input! Please choose from the above given options...'
    LOAD_QUES_MSG = 'Questions Added!'
    MANAGE_CATEGORIES_MSG = '\n----Manage Categories----\n'
    MANAGE_QUES_MSG = '\n----Manage Questions----\n'
    CATEGORIES_MSG = '\n-----Quiz Categories-----\n'
    QUES_NOT_FOUND_MSG = 'No Questions Currently, Please add a question!!'
    QUES_MSG = '\n-----Quiz Questions-----\n'
    QUIZ_DATA_NOT_FOUND_MSG = 'No data! Take a Quiz...'
    LEADERBOARD_MSG = '\n-----Leaderboard-----\n'
    QUIZ_START_MSG = '\n-----Quiz Starting-----\n'
    REVIEW_RESPONSES_MSG = '\n-----REVIEW YOUR RESPONSES-----\n'
    CATEGORY_NOT_FOUND_MSG = 'No such Category! Please choose from above!!'
    USER_NOT_FOUND_MSG = 'No {user} Currently!'
    DISPLAY_USERS_MSG = '\n-----List of {user}s-----\n'
    SCORE_DATA_MSG = '\n-----Score History-----\n'
    HIGHEST_SCORE_MSG = '\nHighest Score: {score}\n'
    CREATE_SUPER_ADMIN_SUCCESS_MSG = 'Super Admin created!'
    INITIALIZATION_SUCCESS_MSG = '\nInitialization Complete!\n'
    USER_WELCOME_MSG = '\n----Welcome {user}----\n'
    MANAGE_PLAYERS_MSG = '\n----Manage Players----\n'
    MANAGE_QUIZ_MSG = '\n----Manage Quizzes----\n'
    DASHBOARD_MSG = '\n----{user} Dashboard----\n'
    INVALID_ROLE_MSG = 'Invalid Role!: '
    TABULATE_ERROR_MSG = 'Could not pretty print...\n'
    TRY_AGAIN_MSG = '\n{error} Please try again...\n'
    INVALID_TEXT = 'Invalid {}'
    INVALID_CHOICE = 'Select a number from above options!'
    INVALID_PASSWORD = 'Invalid password! Length cannot be less than 6!'


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
    SYSTEM_START='app.py running'
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
