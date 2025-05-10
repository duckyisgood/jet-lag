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

    def __init__(self, players):
        self.players = players

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
        penalty = [300, 150, 0]
        self.coins -= penalty[2 - len(self.hand)]  # deduct penalty
        if self.coins < 0:  # coins can't go below 0
            self.coins = 0
        pool = [self.deck.pop() for i in range(3)]  # returns the pool of 3 random cards
        return pool


class Game:
    chasers: Team
    runners: Team

    def __init__(self, total_players, teams: list[str] = None):
        """
        :param total_players: list (even number of people)
        """
        if not teams:
            a = total_players
            random.shuffle(a)
            self.chasers = Team(a[len(a) / 2:])
            self.runners = Team(a[:len(a) / 2])
        else:
            self.chasers = Team(teams[0])
            self.runners = Team(teams[1])

    def switch_sides(self, caught=True):
        if caught:  # deduct points if they were caught
            for i in self.runners.hand:  # deduce challenge points equal the value of the runner's hand
                self.runners.challenge_points -= i.challenge_points
            if self.runners.challenge_points < 0:  # you can't have negative challenge points
                self.runners.challenge_points = 0

        # switch teams
        temp = self.chasers
        self.chasers = self.runners
        self.runners = temp


with open("cards.pkl", 'rb') as file:
    whole_deck: list[Card] = pickle.load(file)

