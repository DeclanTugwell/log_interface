CREATE TABLE account(
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    account_type INTEGER NOT NULL
);

CREATE TABLE project(
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    project_name TEXT UNIQUE NOT NULL,
    FOREIGN KEY (account_id) REFERENCES account (account_id)
);

CREATE TABLE project_user(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hardware_id TEXT UNIQUE NOT NULL,
    project_id INTEGER NOT NULL,
    FOREIGN KEY (project_id) REFERENCES project (project_id)
);

CREATE TABLE user_session(
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES project_user (user_id)
);

CREATE TABLE log(
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    log_type INTEGER NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    FOREIGN KEY (session_id) REFERENCES user_session (session_id)
);