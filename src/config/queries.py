'''Queries for database operations'''


class InitializationQueries:
    '''Contains queries for creation of db tables'''

    CREATE_CATEGORIES_TABLE = '''
        CREATE TABLE IF NOT EXISTS categories (
            category_id VARCHAR(10) PRIMARY KEY,
            admin_id VARCHAR(10),
            admin_username VARCHAR(25),
            category_name VARCHAR(25) UNIQUE
        )'''
    CREATE_CREDENTIALS_TABLE= '''
        CREATE TABLE IF NOT EXISTS credentials (
            user_id VARCHAR(10) PRIMARY KEY,
            username VARCHAR(25) UNIQUE,
            password VARCHAR(100),
            isPasswordChanged INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE
        )'''
    CREATE_OPTIONS_TABLE = '''
        CREATE TABLE IF NOT EXISTS options (
            option_id VARCHAR(10) PRIMARY KEY,
            question_id VARCHAR(10),
            option_text VARCHAR(50),
            isCorrect INTEGER,
            FOREIGN KEY (question_id) REFERENCES questions (question_id) ON DELETE CASCADE ON UPDATE CASCADE
        )'''
    CREATE_QUESTIONS_TABLE = '''
        CREATE TABLE IF NOT EXISTS questions (
            question_id VARCHAR(10) PRIMARY KEY,
            category_id VARCHAR(10),
            admin_id VARCHAR(10),
            admin_username VARCHAR(25),
            question_text VARCHAR(100),
            question_type VARCHAR(25),
            FOREIGN KEY (category_id) REFERENCES categories (category_id) ON DELETE CASCADE ON UPDATE CASCADE
        )'''
    CREATE_SCORES_TABLE = '''
        CREATE TABLE IF NOT EXISTS scores (
            score_id VARCHAR(10) PRIMARY KEY,
            player_id VARCHAR(10),
            score INTEGER,
            timestamp VARCHAR(20),
            FOREIGN KEY (player_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE
        )'''
    CREATE_USERS_TABLE = '''
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR(10) PRIMARY KEY,
            name VARCHAR(50),
            email VARCHAR(50) UNIQUE,
            role VARCHAR(20),
            registration_date VARCHAR(10)
        )'''


class Queries:
    '''Contains database queries'''

    INSERT_CATEGORY = 'INSERT INTO categories VALUES (%s, %s, %s, %s)'
    INSERT_CREDENTIALS = 'INSERT INTO credentials VALUES (%s, %s, %s, %s)'
    INSERT_OPTION = 'INSERT INTO options VALUES (%s, %s, %s, %s)'
    INSERT_QUESTION = 'INSERT INTO questions VALUES (%s, %s, %s, %s, %s, %s)'
    INSERT_USER_DATA = 'INSERT INTO users VALUES (%s, %s, %s, %s, %s)'
    INSERT_PLAYER_QUIZ_SCORE = 'INSERT INTO scores VALUES (%s, %s, %s, %s)'
    GET_ALL_CATEGORIES = '''
        SELECT category_name, admin_username 
        FROM categories ORDER BY category_name'''
    GET_ALL_QUESTIONS_DETAIL = '''
        SELECT category_name, question_text, question_type, option_text, questions.admin_username
        FROM questions 
        INNER JOIN categories ON questions.category_id = categories.category_id
        INNER JOIN options ON questions.question_id = options.question_id
        WHERE options.isCorrect = 1
        ORDER BY category_name
    '''
    GET_CATEGORY_ID_BY_NAME = 'SELECT category_id FROM categories WHERE category_name = %s'
    GET_CREDENTIALS_BY_USERNAME = '''
        SELECT password, role, isPasswordChanged
        FROM credentials INNER JOIN users ON credentials.user_id = users.user_id 
        WHERE username = %s
    '''
    GET_LEADERBOARD = '''
        SELECT username, MAX(score) as max_score, MIN(timestamp) as min_timestamp
        FROM scores
        INNER JOIN credentials ON scores.player_id = credentials.user_id
        GROUP BY username
        ORDER BY max_score DESC, min_timestamp ASC
        LIMIT 10
    '''
    GET_OPTIONS_FOR_MCQ = 'SELECT option_text FROM options WHERE question_id = %s ORDER BY RAND()'
    GET_QUESTIONS_BY_CATEGORY = '''
        SELECT question_text, question_type, option_text, questions.admin_username
        FROM questions 
        INNER JOIN categories ON questions.category_id = categories.category_id
        INNER JOIN options ON questions.question_id = options.question_id
        WHERE options.isCorrect = 1 AND category_name = %s
    '''
    GET_RANDOM_QUESTIONS = '''
        SELECT questions.question_id, question_text, question_type, option_text
        FROM questions
        INNER JOIN options ON questions.question_id = options.question_id
        WHERE options.isCorrect = 1
        ORDER BY RAND() LIMIT 10
    '''
    GET_RANDOM_QUESTIONS_BY_CATEGORY = '''
        SELECT questions.question_id, question_text, question_type, option_text
        FROM questions 
        INNER JOIN categories ON questions.category_id = categories.category_id
        INNER JOIN options ON questions.question_id = options.question_id
        WHERE options.isCorrect = 1 AND category_name = %s
        ORDER BY RAND() LIMIT 10
    '''
    GET_USER_BY_ROLE = '''
        SELECT username, name, email, registration_date
        FROM users INNER JOIN credentials ON users.user_id = credentials.user_id
        WHERE role = %s
    '''
    GET_USER_BY_USERNAME = '''
        SELECT username, name, email, registration_date
        FROM users 
        INNER JOIN credentials ON users.user_id = credentials.user_id
        WHERE username = %s
    '''
    GET_USER_ID_BY_USERNAME = '''
        SELECT users.user_id
        FROM users 
        INNER JOIN credentials ON users.user_id = credentials.user_id
        WHERE username = %s
    '''
    GET_PLAYER_SCORES_BY_USERNAME = '''
        SELECT timestamp, score 
        FROM scores 
        INNER JOIN credentials ON scores.player_id = credentials.user_id
        WHERE username = %s
        ORDER BY timestamp DESC
    '''
    UPDATE_ADMIN_PASSWORD_BY_USERNAME = '''
        UPDATE credentials 
        SET password = %s, isPasswordChanged = %s 
        WHERE username = %s
    '''
    UPDATE_CATEGORY_BY_NAME = 'UPDATE categories SET category_name = %s WHERE category_name = %s'
    UPDATE_QUESTION_TEXT_BY_ID = 'UPDATE questions SET question_text = %s WHERE question_id = %s'
    DELETE_CATEGORY_BY_NAME = 'DELETE FROM categories WHERE category_name = %s'
    DELETE_QUESTION_BY_ID = 'DELETE FROM questions WHERE question_id = %s'
    DELETE_USER_BY_EMAIL = 'DELETE FROM users WHERE email = %s'
