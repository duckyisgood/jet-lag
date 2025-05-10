from flask import Flask, render_template, request, redirect, url_for, session
import random
import pandas as pd
from logic import Card, Challenge, Curse, PowerUp, Team, Game, powerups, whole_deck

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session storage

# ----------------------
# Load and Parse Cards
# ----------------------
csv_file = "JLTST Card Ideas - Total.csv"
df = pd.read_csv(csv_file)


# ----------------------
# Game State Management
# ----------------------


game = Game()
runner = game.runners
chaser = game.chasers

# ----------------------
# Flask Routes
# ----------------------
@app.route('/')
def index():
    return render_template('game.html', team=runner, shop=powerups)


@app.route('/draw', methods=['POST'])
def draw():
    draw_pool = runner.drawChallenge()  # Calls your draw logic in Team
    if draw_pool:
        # Save the draw results in session so frontend can display them
        session['draw_pool'] = [(c.title, c.text, c.challenge_points, c.coins) for c in draw_pool]
    return redirect(url_for('index'))


@app.route('/select_card', methods=['POST'])
def select_card():
    title = request.form['card_title']
    for c in whole_deck:
        if c.title == title:
            runner.addCard(c)
            break
    session.pop('draw_pool', None)
    return redirect(url_for('index'))


@app.route('/switch', methods=['POST'])
def switch():
    global runner, chaser
    runner, chaser = chaser, runner
    game.switch_sides()
    return redirect(url_for('index'))


@app.route('/shop', methods=['POST'])
def shop():
    powerup_title = request.form['powerup']
    runner.buy_powerup(powerup_title)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
