import pickle
import random


class Card:
    challenge_points: int
    coins: int
    title: str
    text: str
    type: str

    def __init__(self, title, text, c_points, coins):
        self.challenge_points = c_points
        self.coins = coins
        self.title = title
        self.text = text

    def __repr__(self):
        return f"{self.type}: {self.title}"


class Challenge(Card):
    """
    tiers = list: [[t1C_points, t1Coins], [t2C_points, t2Coins]]
    """
    tiers: list
    title: str
    type = "challenge"

    def __init__(self, title, text, c_points, coins, tiers):
        super().__init__(title, text, c_points, coins)
        self.tiers = tiers

    def selected_tier(self, tier: int):
        """Modifies the challenge for the selected tier"""
        self.challenge_points = self.tiers[tier][0]
        self.coins = self.tiers[tier][1]


class PowerUp(Card):
    type = "powerup"

    def __init__(self, title, text, c_points, coins):
        super().__init__(title, text, c_points, coins)


class Curse(Card):
    type = "curse"

    def __init__(self, title, text, c_points, coins):
        super().__init__(title, text, c_points, coins)


class Team:
    challenge_points: int = 0
    coins: int = 0
    hand: list[Challenge] = []
    completed_challenges: list[Challenge] = []
    deck: list[Card]
    players: list[str]
    team_type: str

    def __init__(self, players: list[str] = None, team_type = "runners"):
        self.players = players
        self.team_type = team_type

    def startRun(self):
        self.deck = whole_deck
        random.shuffle(self.deck)
        self.hand = []

    def completeChallenge(self, challenge: Challenge):
        """Simulates a challenge completion"""
        if challenge not in self.hand:
            return False
        self.coins += challenge.coins
        self.challenge_points += challenge.challenge_points
        self.hand.remove(challenge)
        return True

    def payPowerUp(self, powerUp):
        """Pays for a power up"""
        self.coins -= powerUp.coins
        self.challenge_points -= powerUp.challenge_points

    def modifyPoints(self, coins=0, c_points=0, challenge=None):
        """Modifies the amount of coins, challenge points, and your hand"""
        self.coins += coins
        self.challenge_points += c_points
        self.hand.remove(challenge)

    def drawChallenge(self):
        """
        Simulates drawing a challenge, deducts penalty
        :return: card pool
        """
        if len(self.hand) >= 3:
            return False
        penalty = [0, 150, 300]
        self.coins -= penalty[len(self.hand)]  # deduct penalty
        if self.coins < 0:  # coins can't go below 0
            self.coins = 0
        pool = [self.deck.pop() for _ in range(3)]  # returns the pool of 3 random cards
        return pool

    def addCard(self, card):
        self.hand.append(card)

    def cursed(self, curse: Curse):
        self.coins += curse.coins
        self.challenge_points += curse.challenge_points

    def buy_powerup(self, p):
        if self.coins >= p.coins:
            self.coins -= p.coins
            self.challenge_points -= p.challenge_points
            return True
        else:
            return False


class Game:
    chasers: Team(team_type="chasers")
    runners: Team(team_type="runners")

    def __init__(self, total_players=0, teams: list[str] = None):
        """
        :param total_players: list (even number of people)
        """
        self.chasers = Team()
        self.runners = Team()
        # if not teams:
        #     a = total_players
        #     random.shuffle(a)
        #     self.chasers = Team(a[len(a) / 2:])
        #     self.runners = Team(a[:len(a) / 2])
        # else:
        #     self.chasers = Team(players=teams[0])
        #     self.runners = Team(teams[1])

    def switch_sides(self, caught=True):
        if caught:  # deduct points if they were caught
            for i in self.runners.hand:  # deduce challenge points equal the value of the runner's hand
                self.runners.challenge_points -= i.challenge_points
            if self.runners.challenge_points < 0:  # you can't have negative challenge points
                self.runners.challenge_points = 0
            self.chasers.startRun()

        # switch teams
        temp = self.chasers
        self.chasers = self.runners
        self.runners = temp


with open("cards.pkl", 'rb') as file:
    cards = pickle.load(file)
whole_deck = cards[1]
powerups = cards[0]