from datetime import datetime
import json
from flask import Flask, flash, jsonify, render_template, request
from sqlalchemy import create_engine, text
from database import load_acc_from_db, load_games_from_db, add_acc_in_db, add_game_in_db

app = Flask(__name__)
app.secret_key = '123'

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/newaccount", methods=['get', 'post'])
def newAccount():
    return render_template('newaccount.html')

@app.route("/confirmaccount", methods=['get', 'post'])
def confirmAccount():
    ACCOUNTS = load_acc_from_db()

    for acc in ACCOUNTS:
        if acc['username'] == request.form['username']:
            flash('Username Taken')
            return render_template('newaccount.html')

    if request.form['password'] == request.form['confirm_password']:
        ACCOUNTS.append({
            'username': request.form['username'],
            'password': request.form['password']
        })
        add_acc_in_db(ACCOUNTS)
        return render_template('home.html')
    
    flash('Passwords Do Not Match')
    return render_template('newaccount.html')

    

@app.route("/tracker", methods=['post', 'get'])
def tracker():
    ACCOUNTS = load_acc_from_db()
    GAMES = load_games_from_db()
    data = request.form

    for acc in ACCOUNTS:
        if acc['username'] == data['username'] and acc['password'] == data['password']:
            for elem in GAMES:
                if elem['username'] == data['username']:
                    return render_template('tracker.html', games=reversed(elem['games']), username=data['username'])
            return render_template('tracker.html', games=[], username=data['username'])
    
    flash('Incorrect Username or Password', 'error')
    return render_template('home.html')

@app.route("/tracker/game/end", methods=['post', 'get'])
def trackerGameEnd():
    GAMES = load_games_from_db()
    username = request.form['username']

    for elem in GAMES:
        if elem['username'] == username:
            return render_template('tracker.html', games=reversed(elem['games']), username=username)

@app.route("/tracker/game", methods=['post', 'get'])
def game():
    GAMES = load_games_from_db()
    username = request.form['username']
    teamname1 = request.form['teamname1']
    teamname2 = request.form['teamname2']
    dt = datetime.now()
    id = dt.strftime("%d/%m/%Y %H:%M:%S")

    for elem in GAMES:
        if elem['username'] == username:
            elem['games'].append({'id': id, 'teamname1':teamname1, 'teamname2':teamname2,'team1':0, 'team2':0, 'runs1':[], 'runs2':[]})
            add_game_in_db(username, GAMES)
            return render_template('game.html', teamname1=teamname1, teamname2=teamname2, team1=0, team2=0, runs1=[], runs2=[], id=id, username=username)

    GAMES.append(
        {
            'username': username,
            'games': [
                {
                    'id':id,
                    'teamname1':teamname1,
                    'teamname2':teamname2,
                    'team1':0,
                    'team2':0,
                    'runs1':[],
                    'runs2':[]
                }
            ]
        }
    )
    
    add_game_in_db(username, GAMES)
    return render_template('game.html', teamname1=teamname1, teamname2=teamname2, team1=0, team2=0, runs1=[], runs2=[], id=id, username=username)

@app.route("/tracker/resume", methods=['post', 'get'])
def gameResume():
    GAMES = load_games_from_db()
    username = request.form['username']
    id = request.form['id']

    for elem in GAMES:
        if elem['username'] == username:
            for game in elem['games']:
                if game['id'] == id:
                    return render_template('game.html', teamname1=game['teamname1'], teamname2=game['teamname2'], team1=game['team1'], team2=game['team2'], runs1=game['runs1'], runs2=game['runs2'], id=id, username=username)

@app.route("/tracker/game/add", methods=['post', 'get'])
def trackerGameRun():
    GAMES = load_games_from_db()
    id = request.form['id']
    team = request.form['team']
    username = request.form['username']
    runs = request.form['runs']

    for elem in GAMES:
        if elem['username'] == username:
            for game in elem['games']:
                if str(game['id']) == id:
                    if team == "team1":
                        game['team1'] += int(runs)
                        game['runs1'].append(int(runs))
                        add_game_in_db(username, GAMES)
                        return render_template('game.html', teamname1=game['teamname1'], teamname2=game['teamname2'], team1=game['team1'], team2=game['team2'], runs1=game['runs1'], runs2=game['runs2'], id=id, username=username)
                    elif team == "team2":
                        game['team2'] += int(runs)
                        game['runs2'].append(int(runs))
                        add_game_in_db(username, GAMES)
                        return render_template('game.html', teamname1=game['teamname1'], teamname2=game['teamname2'], team1=game['team1'], team2=game['team2'], runs1=game['runs1'], runs2=game['runs2'], id=id, username=username)

@app.route("/tracker/game/undo", methods=['post', 'get'])
def trackerGameRunUndo():
    GAMES = load_games_from_db()
    id = request.form['id']
    team = request.form['team']
    username = request.form['username']

    for elem in GAMES:
        if elem['username'] == username:
            for game in elem['games']:
                if str(game['id']) == id:
                    if team == "team1":
                        if len(game['runs1']) > 0:
                            game['team1'] -= game['runs1'].pop()
                        else:
                            return render_template('game.html', teamname1=game['teamname1'], teamname2=game['teamname2'], team1=game['team1'], team2=game['team2'], runs1=game['runs1'], runs2=game['runs2'], id=id, username=username)
                        add_game_in_db(username, GAMES)
                        return render_template('game.html', teamname1=game['teamname1'], teamname2=game['teamname2'], team1=game['team1'], team2=game['team2'], runs1=game['runs1'], runs2=game['runs2'], id=id, username=username)
                    elif team == "team2":
                        if len(game['runs2']) > 0:
                            game['team2'] -= game['runs2'].pop()
                        else:
                            return render_template('game.html', teamname1=game['teamname1'], teamname2=game['teamname2'], team1=game['team1'], team2=game['team2'], runs1=game['runs1'], runs2=game['runs2'], id=id, username=username)
                        add_game_in_db(username, GAMES)
                        return render_template('game.html', teamname1=game['teamname1'], teamname2=game['teamname2'], team1=game['team1'], team2=game['team2'], runs1=game['runs1'], runs2=game['runs2'], id=id, username=username)

@app.route("/tracker/delete", methods=['post', 'get'])
def trackerGameDel():
    GAMES = load_games_from_db()
    id = request.form['id']
    username = request.form['username']
    orig_games = []

    for elem in GAMES:
        if elem['username'] == username:
            orig_games = elem['games']
            for game in elem['games']:
                if str(game['id']) == id:
                    elem['games'].remove(game)
                    add_game_in_db(username, GAMES)
                    return render_template('tracker.html', games=reversed(elem['games']), username=username)
    
    return render_template('tracker.html', games=reversed(orig_games), username=username)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)