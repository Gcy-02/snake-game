from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

def init_db():
    if not os.path.exists('scores.db'):
        conn = sqlite3.connect('scores.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE scores
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      player_name TEXT NOT NULL,
                      score INTEGER NOT NULL,
                      date TEXT NOT NULL)''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('SELECT * FROM scores ORDER BY score DESC LIMIT 10')
    scores = c.fetchall()
    conn.close()
    return render_template('index.html', scores=scores)

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/api/save_score', methods=['POST'])
def save_score():
    data = request.get_json()
    player_name = data.get('player_name', '匿名玩家')
    score = data.get('score', 0)
    
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('INSERT INTO scores (player_name, score, date) VALUES (?, ?, datetime("now"))',
              (player_name, score))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/get_scores')
def get_scores():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('SELECT * FROM scores ORDER BY score DESC LIMIT 10')
    scores = c.fetchall()
    conn.close()
    
    result = []
    for row in scores:
        result.append({
            'id': row[0],
            'player_name': row[1],
            'score': row[2],
            'date': row[3]
        })
    
    return jsonify(result)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
