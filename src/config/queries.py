'''Queries for database operations'''


class InitializationQueries:
    '''Contains queries for creation of db tables'''

    CREATE_DATABASE = 'CREATE DATABASE IF NOT EXISTS {}'
    USE_DATABASE = 'USE {}'
    CREATE_CATEGORIES_TABLE = '''
        CREATE TABLE IF NOT EXISTS categories (
            category_id VARCHAR(10) PRIMARY KEY,
            admin_id VARCHAR(10),
            category_name VARCHAR(50) UNIQUE
        )'''
    CREATE_CREDENTIALS_TABLE = '''
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
            option_text VARCHAR(100),
            isCorrect INTEGER,
            FOREIGN KEY (question_id) REFERENCES questions (question_id) ON DELETE CASCADE ON UPDATE CASCADE
        )'''
    CREATE_QUESTIONS_TABLE = '''
        CREATE TABLE IF NOT EXISTS questions (
            question_id VARCHAR(10) PRIMARY KEY,
            category_id VARCHAR(10),
            admin_id VARCHAR(10),
            question_text VARCHAR(250) UNIQUE,
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
    CREATE_TOKEN_TABLE = '''
        CREATE TABLE IF NOT EXISTS tokens (
            user_id VARCHAR(10),
            access_token VARCHAR(100) PRIMARY KEY,
            refresh_token VARCHAR(100) UNIQUE NOT NULL,
            status VARCHAR(20) DEFAULT "active",
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE
        )
    '''


class Queries:
    '''Contains database queries'''

    INSERT_CATEGORY = 'INSERT INTO categories VALUES (%s, %s, %s)'
    INSERT_CREDENTIALS = 'INSERT INTO credentials VALUES (%s, %s, %s, %s)'
    INSERT_OPTION = 'INSERT INTO options VALUES (%s, %s, %s, %s)'
    INSERT_QUESTION = 'INSERT INTO questions VALUES (%s, %s, %s, %s, %s)'
    INSERT_USER_DATA = 'INSERT INTO users VALUES (%s, %s, %s, %s, %s)'
    INSERT_PLAYER_QUIZ_SCORE = 'INSERT INTO scores VALUES (%s, %s, %s, %s)'
    INSERT_TOKEN_DATA = 'INSERT INTO tokens (user_id, access_token, refresh_token) VALUES (%s, %s, %s)'
    GET_USERNAME = 'SELECT username FROM credentials WHERE username = %s'
    GET_ALL_CATEGORIES = '''
        SELECT *
        FROM categories ORDER BY category_name'''
    GET_ALL_QUESTIONS_DETAIL = '''
        SELECT category_name, question_text, question_type, option_text as answer, questions.admin_username
        FROM questions 
        INNER JOIN categories ON questions.category_id = categories.category_id
        INNER JOIN options ON questions.question_id = options.question_id
        WHERE options.isCorrect = 1
        ORDER BY category_name
    '''
    GET_QUIZ_DATA = '''
        SELECT
            c.category_id,
            c.category_name,
            c.admin_id as category_creator_id,
            q.question_id,
            q.question_text,
            q.admin_id as question_creator_id,
            q.question_type,
            o.option_text,
            o.isCorrect
        FROM Categories c
        JOIN Questions q ON c.category_id = q.category_id
        LEFT JOIN Options o ON q.question_id = o.question_id
    '''
    GET_CATEGORY_ID_BY_NAME = 'SELECT category_id FROM categories WHERE category_name = %s'
    GET_CREDENTIALS_BY_USERNAME = '''
        SELECT credentials.user_id, password, role, isPasswordChanged
        FROM credentials INNER JOIN users ON credentials.user_id = users.user_id 
        WHERE username = %s
    '''
    GET_PASSWORD_BY_USER_ID = '''SELECT password FROM credentials WHERE user_id = %s'''
    GET_LEADERBOARD = '''
        SELECT player_id, username, MAX(score) as score, MIN(timestamp) as timestamp
        FROM scores
        INNER JOIN credentials ON scores.player_id = credentials.user_id
        GROUP BY player_id
        ORDER BY score DESC, timestamp ASC
        LIMIT 10
    '''
    GET_OPTIONS_FOR_MCQ = 'SELECT option_text FROM options WHERE question_id = %s ORDER BY RAND()'
    GET_QUESTIONS_BY_CATEGORY = '''
        SELECT question_text, question_type, option_text as answer, questions.admin_username
        FROM questions 
        INNER JOIN categories ON questions.category_id = categories.category_id
        INNER JOIN options ON questions.question_id = options.question_id
        WHERE options.isCorrect = 1 AND categories.category_id = %s
    '''
    GET_RANDOM_QUESTIONS_BY_CATEGORY = '''
        SELECT q.question_id, q.question_text, q.question_type, GROUP_CONCAT(o.option_text) as options
        FROM Questions q
        LEFT JOIN Options o ON q.question_id = o.question_id
        WHERE (q.category_id = %s OR %s IS NULL OR q.category_id IS NULL)
        AND (q.question_type = %s OR %s IS NULL OR q.question_type IS NULL)
        GROUP BY q.question_id
        ORDER BY RAND() LIMIT %s;
    '''
    GET_USER_BY_ROLE = '''
        SELECT users.user_id, username, name, email, registration_date
        FROM users INNER JOIN credentials ON users.user_id = credentials.user_id
        WHERE role = %s
    '''
    GET_USER_BY_USER_ID = '''
        SELECT username, name, email, registration_date
        FROM users 
        INNER JOIN credentials ON users.user_id = credentials.user_id
        WHERE users.user_id = %s
    '''
    GET_USER_ID_BY_USERNAME = '''
        SELECT users.user_id
        FROM users 
        INNER JOIN credentials ON users.user_id = credentials.user_id
        WHERE username = %s
    '''
    GET_PLAYER_SCORES_BY_ID = '''
        SELECT score_id, score, timestamp
        FROM scores 
        INNER JOIN credentials ON scores.player_id = credentials.user_id
        WHERE scores.player_id = %s
        ORDER BY timestamp DESC
    '''
    GET_QUESTION_DATA_BY_QUESTION_ID = '''
        SELECT q.question_id, q.question_text, o.option_text as correct_answer
        FROM questions q
        LEFT JOIN options o ON q.question_id = o.question_id AND o.isCorrect = 1
        WHERE q.question_id IN (%s)
    '''
    GET_ACCESS_TOKEN_STATUS = 'SELECT status FROM tokens WHERE access_token = %s'
    GET_REFRESH_TOKEN_STATUS = 'SELECT status FROM tokens WHERE refresh_token = %s'
    UPDATE_ADMIN_PASSWORD_BY_USERNAME = '''
        UPDATE credentials 
        SET password = %s, isPasswordChanged = %s 
        WHERE username = %s
    '''
    UPDATE_CATEGORY_BY_NAME = 'UPDATE categories SET category_name = %s WHERE category_name = %s'
    UPDATE_CATEGORY_BY_ID = 'UPDATE categories SET category_name = %s WHERE category_id = %s'
    UPDATE_QUESTION_TEXT_BY_ID = 'UPDATE questions SET question_text = %s WHERE question_id = %s'
    UPDATE_USER_PROFILE = 'UPDATE users SET name = %s, email = %s WHERE user_id = %s'
    UPDATE_USERNAME = 'UPDATE credentials SET username = %s WHERE user_id = %s'
    UPDATE_USER_PASSWORD = 'UPDATE credentials SET password = %s, isPasswordChanged = 1 WHERE user_id = %s'
    UPDATE_TOKEN_STATUS = 'UPDATE tokens SET status = "revoked" WHERE user_id = %s'
    DELETE_CATEGORY_BY_NAME = 'DELETE FROM categories WHERE category_name = %s'
    DELETE_CATEGORY_BY_ID = 'DELETE FROM categories WHERE category_id = %s'
    DELETE_QUESTION_BY_ID = 'DELETE FROM questions WHERE question_id = %s'
    DELETE_USER_BY_EMAIL = 'DELETE FROM users WHERE email = %s'
    DELETE_USER_BY_ID_ROLE = 'DELETE FROM users WHERE user_id = %s and role = %s'
