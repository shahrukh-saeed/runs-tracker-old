import json
from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(
    db_connection_string, 
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem",
            }
        })

def load_acc_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from accounts"))
        result_all_acc = result.all()
        dict_acc = dict(result_all_acc)
        accounts = []

        for username in dict_acc:
            password = dict_acc[username]
            accounts.append({'username': username, 'password': password})

        return accounts

def load_games_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from games"))
        result_all_games = result.all()
        dict_games = dict(result_all_games)
        games = []

        for username in dict_games:
            gamesinfo = json.loads(dict_games[username])
            games.append({'username': username, 'games': gamesinfo})

        return games

def add_acc_in_db(ACCOUNTS):
    with engine.connect() as conn:
        for acc in ACCOUNTS:
            username = acc['username']
            password = acc['password']
            conn.execute(text(f"insert ignore into accounts (username, password) values ('{username}', '{password}')"))

def add_game_in_db(username, GAMES):
    with engine.connect() as conn:
        for elem in GAMES:
            if elem['username'] == username:
                games = json.dumps(elem['games'])
                conn.execute(text(f"INSERT INTO games (username, games) VALUES ('{username}', '{games}') ON DUPLICATE KEY UPDATE games = '{games}'"))

