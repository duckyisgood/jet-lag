import pandas as pd
from jltst_full import Challenge, Card, PowerUp, Curse
import pickle

# Load your CSV file
df = pd.read_csv("JLTST Card Ideas - Total.csv")

# Initialize containers
challenges = []
powerups = []
curses = []
cards = []

# Section-aware parsing
current_section = None
i = 0

while i < len(df):
    row = df.iloc[i]
    title = str(row['Card Name']).strip()

    # Detect section headers
    if title in ['Challenges', 'Power-Ups', 'Curses']:
        current_section = title
        i += 1
        continue

    # Skip rows with missing values
    if pd.isna(row['Coin price/Coins earned']) or pd.isna(row['Challenge point price/earned']):
        i += 1
        continue

    # Handle Challenge cards (with tiers)
    if current_section == 'Challenges' and not title.startswith('-'):
        text = str(row['Effect']).strip()
        tiers = [[int(row['Challenge point price/earned']), int(row['Coin price/Coins earned'])]]

        # Check for tiered rows
        j = i + 1
        while j < len(df) and str(df.iloc[j]['Card Name']).strip().startswith('-'):
            sub = df.iloc[j]
            tiers.append([int(sub['Challenge point price/earned']), int(sub['Coin price/Coins earned'])])
            j += 1

        challenges.append(Challenge(title, text, tiers[0][0], tiers[0][1], tiers))
        i = j

    # Handle PowerUps
    elif current_section == 'Power-Ups':
        text = str(row['Effect']).strip()
        powerups.append(PowerUp(title, text, int(row['Challenge point price/earned']), int(row['Coin price/Coins earned'])))
        i += 1

    # Handle Curses
    elif current_section == 'Curses':
        text = str(row['Effect']).strip()
        curses.append(Curse(title, text, int(row['Challenge point price/earned']), int(row['Coin price/Coins earned'])))
        i += 1

    else:
        i += 1  # Safety fallback


for i in challenges:
    cards.append(("ch", i))
for i in powerups:
    cards.append(("p", i))
for i in curses:
    cards.append(("cu", i))


with open("cards.pkl", 'wb') as file:
    pickle.dump(cards, file)
