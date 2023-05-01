from datetime import datetime
import random
from flask import Flask, flash, jsonify, render_template, request

app = Flask(__name__)
app.secret_key = '123'

ACCOUNTS = [
    {
        'username': 'test1',
        'password': '1',
    }
]

GAMES = [
    {
        'username': 'test1',
        'games': [
            {
                'id': "1",
                'teamname1': "A",
                'teamname2': "B",
                'team1': 50,
                'team2': 60,
                'runs1': [1, 2, 4, 6, 2, 1],
                'runs2': [1, 4, 6]
            },
            {
                'id': "2",
                'teamname1': "C",
                'teamname2': "D",
                'team1': 70,
                'team2': 80,
                'runs1': [1, 2, 4, 6, 2, 1],
                'runs2': [1, 4, 6]
            }
        ]
    }
]

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/newaccount", methods=['get', 'post'])
def newAccount():
    return render_template('newaccount.html')

@app.route("/confirmaccount", methods=['get', 'post'])
def confirmAccount():
    ACCOUNTS.append(request.form)
    return render_template('home.html')

@app.route("/tracker", methods=['post', 'get'])
def tracker():
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
    username = request.form['username']

    for elem in GAMES:
        if elem['username'] == username:
            return render_template('tracker.html', games=reversed(elem['games']), username=username)

@app.route("/tracker/game", methods=['post', 'get'])
def game():
    username = request.form['username']
    teamname1 = request.form['teamname1']
    teamname2 = request.form['teamname2']
    dt = datetime.now()
    id = dt.strftime("%d/%m/%Y %H:%M:%S")

    for elem in GAMES:
        if elem['username'] == username:
            elem['games'].append({'id': id, 'teamname1':teamname1, 'teamname2':teamname2,'team1':0, 'team2':0, 'runs1':[], 'runs2':[]})
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
    
    return render_template('game.html', teamname1=teamname1, teamname2=teamname2, team1=0, team2=0, runs1=[], runs2=[], id=id, username=username)

@app.route("/tracker/game/add", methods=['post', 'get'])
def trackerGameRun():
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
                        return render_template('game.html', teamname1=game['teamname1'], teamname2=game['teamname2'], team1=game['team1'], team2=game['team2'], runs1=game['runs1'], runs2=game['runs2'], id=id, username=username)
                    elif team == "team2":
                        game['team2'] += int(runs)
                        game['runs2'].append(int(runs))
                        return render_template('game.html', teamname1=game['teamname1'], teamname2=game['teamname2'], team1=game['team1'], team2=game['team2'], runs1=game['runs1'], runs2=game['runs2'], id=id, username=username)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)