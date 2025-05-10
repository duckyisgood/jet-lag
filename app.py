from flask import Flask, render_template, request, redirect, url_for, session
import random
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session storage

# ----------------------
# Load and Parse Cards
# ----------------------
csv_file = "JLTST Card Ideas - Total.csv"
df = pd.read_csv(csv_file)


class Card:
    def __init__(self, title, text, c_points, coins):
        self.title = title
        self.text = text
        self.challenge_points = c_points
        self.coins = coins


class Challenge(Card):
    def __init__(self, title, text, c_points, coins, tiers):
        super().__init__(title, text, c_points, coins)
        self.tiers = tiers


class PowerUp(Card):
    pass


class Curse(Card):
    pass


challenges = []
powerups = []
curses = []

section = None
i = 0

while i < len(df):
    row = df.iloc[i]
    title = str(row['Card Name']).strip()

    if title.lower() in ['challenges', 'powerups', 'curses']:
        section = title.lower()
        i += 1
        continue

    if pd.isna(row['Coin price/Coins earned']) or pd.isna(row['Challenge point price/earned']):
        i += 1
        continue

    if section == 'challenges' and not title.startswith('-'):
        text = str(row['Effect']).strip()
        tiers = [[int(row['Challenge point price/earned']), int(row['Coin price/Coins earned'])]]
        j = i + 1
        while j < len(df) and str(df.iloc[j]['Card Name']).strip().startswith('-'):
            sub = df.iloc[j]
            tiers.append([int(sub['Challenge point price/earned']), int(sub['Coin price/Coins earned'])])
            j += 1
        challenges.append(Challenge(title, text, tiers[0][0], tiers[0][1], tiers))
        i = j
    elif section == 'powerups':
        text = str(row['Effect']).strip()
        powerups.append(
            PowerUp(title, text, int(row['Challenge point price/earned']), int(row['Coin price/Coins earned'])))
        i += 1
    elif section == 'curses':
        text = str(row['Effect']).strip()
        curses.append(Curse(title, text, int(row['Challenge point price/earned']), int(row['Coin price/Coins earned'])))
        i += 1
    else:
        i += 1


# ----------------------
# Game State Management
# ----------------------
class Team:
    def __init__(self):
        self.hand = []
        self.deck = random.sample(challenges, len(challenges))
        self.coins = 0
        self.points = 0

    def draw(self):
        if len(self.hand) >= 3:
            return None
        penalty = [0, 150, 300]
        cost = penalty[len(self.hand)]
        self.coins -= cost
        draw_pool = [self.deck.pop() for _ in range(3)]
        return draw_pool

    def add_card(self, card):
        self.hand.append(card)
        self.points += card.challenge_points
        self.coins += card.coins

    def buy_powerup(self, powerup_title):
        for p in powerups:
            if p.title == powerup_title:
                if self.coins >= p.coins:
                    self.coins -= p.coins
                    self.points -= p.challenge_points
                    return p
        return None


runner = Team()
chaser = Team()


# ----------------------
# Flask Routes
# ----------------------
@app.route('/')
def index():
    return render_template('game.html', team=runner, shop=powerups)


@app.route('/draw', methods=['POST'])
def draw():
    draw_pool = runner.draw()
    session['draw_pool'] = [(c.title, c.text, c.challenge_points, c.coins) for c in draw_pool]
    return redirect(url_for('index'))


@app.route('/select_card', methods=['POST'])
def select_card():
    title = request.form['card_title']
    for c in challenges:
        if c.title == title:
            runner.add_card(c)
            break
    session.pop('draw_pool', None)
    return redirect(url_for('index'))


@app.route('/switch', methods=['POST'])
def switch():
    global runner, chaser
    runner, chaser = chaser, runner
    return redirect(url_for('index'))


@app.route('/shop', methods=['POST'])
def shop():
    powerup_title = request.form['powerup']
    runner.buy_powerup(powerup_title)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
