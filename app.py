from flask import Flask, flash, jsonify, render_template, request

app = Flask(__name__)
app.secret_key = '123'

ACCOUNTS = [
    {
        'username': 'test1',
        'password': '1',
    },
    {
        'username': 'test2',
        'password': '2'
    }
]

GAMES = [
    {
        'username': 'test1',
        'games': [
            {
                'id': 1,
                'team1': 50,
                'team2': 60
            },
            {
                'id': 2,
                'team1': 70,
                'team2': 80
            }
        ]
    },
    {
        'username': 'test2',
        'games': [
            {
                'id': 2,
                'team1': 35,
                'team2': 30
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

@app.route("/tracker", methods=['post'])
def tracker():
    data = request.form

    for acc in ACCOUNTS:
        if acc['username'] == data['username'] and acc['password'] == data['password']:
            return render_template('tracker.html', games=GAMES, username=data['username'])
    
    flash('Incorrect Username or Password', 'error')
    return render_template('home.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)