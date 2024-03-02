import random

# SETTING GLOBAL VARIABLES

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

# CREATING A CARD CLASS

class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        
    def __str__(self):
        return self.rank + " of " + self.suit

# CREATING A DECK CLASS
# STARTS AS AN EMPTY LIST, CREATES ALL THE CARD FOR EVERY SUIT, EVERY RANK
# WE WANT TO BE ABLE TO SHUFFLE THE DECK
# WE WANT TO BE ABLE TO DEAL ONE CARD FROM THE DECK

class Deck:
    
    def __init__(self):
        self.all_cards = []
        
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.all_cards.append(created_card)
    
    def shuffle(self):
        random.shuffle(self.all_cards)
    
    def deal_one(self):
        return self.all_cards.pop()

# CREATING THE HANDS CLASS
# STARTS AS 0, SUMS THE VALUES
# HIT: ADD CARD

class Hand:
    
    def __init__(self, name):
        self.name = name
        self.all_cards = []
        self.score = []
        
    def add_card(self,card):
        self.all_cards.append(card)
        
        # KEEPING SCORE
        self.score.append(card.value)
        for card in range(len(self.score)):
            if self.score[card]==11 and sum(self.score) > 21:
                self.score[card]=1
                break # IF NO BREAK WITH TWO ACES, BOTH WOULD BE TURNED INTO 1 VALUE!
        
    def __str__(self):
        return f'{self.name} currently has {len(self.all_cards)} cards.'

# CREATING THE CHIPS CLASS

class Chips:

    def __init__(self,name,balance):
        self.name = name
        self.balance = balance
        self.bet = 0

    def win_bet(self):
        
        self.balance += self.bet

    def lose_bet(self):

        self.balance -= self.bet

    def __str__(self):
        return(f"{self.name} has {self.balance} $.")

# GAME FUNCTIONS

def starting_money():
    while True:
        try:
            balance = int(input("How much money did you come with? "))
            while balance < 0:
                balance = int(input("I guess if you have any money, it should be more than 0, right? So how much is it? "))
                return balance
            return balance
        except ValueError:
            print("Invalid input, please enter a number!\n")
            continue

def bet():
    while True:
        try:
            account.bet = int(input("How much money are you willing to risk this round? "))
            while account.bet < 0:
                account.bet = int(input("You know when you bet you gotta enter a positive number... "))
            while account.bet > account.balance:
                account.bet = int(input(f"Not enough money! The maximum bet is {account.balance}. "))
            return account.bet
        except ValueError:
            print("Invalid input, please enter a number!\n")
            continue

    print("Bet accepted.\n")

def deal_cards():
    for card in range(0,2):
        player.add_card(deck.deal_one())
        dealer.add_card(deck.deal_one())
    print(f"\n{name} and the Dealer both have their cards.")
    
def print_player():
    print(player)
    for card in player.all_cards:
        print(card)
    print(f"{name}'s score is " + str(sum(player.score)) + ".\n")
    
def print_dealer_first():
    print(dealer)
    print(f"The Dealer's first card is {dealer.all_cards[0]}.\n")
    
def print_dealer():
    print(dealer)
    for card in dealer.all_cards:
        print(card)
    print(f"The Dealer's score is " + str(sum(dealer.score)) + ".\n")
    
def player_hit(): # PLAYER PICKS ONE MORE CARD
    player.add_card(deck.deal_one())
    print_player()
    
def dealer_hit(): # DEALER PICKS ONE MORE CARD
    dealer.add_card(deck.deal_one())
    print_dealer()
    
def player_busts():
    print(f"The score is more than 21! {name} has lost this round.")
    account.lose_bet()
    
def dealer_busts():
    print(f"The Dealer's score is more than 21! {name} wins this round.")
    account.win_bet()
    
def player_wins():
    print(f"{name} has more (or equal) points than the Dealer! {name} wins this round.")
    account.win_bet()
    
def player_loses():
    print(f"The Dealer has more points than {name}! {name} has lost this round.")
    account.lose_bet()
    
def play_again():
    if input("Do you want to play again? Y/N ") in ['y','Y']:
        return True

# __GAMEPLAY__

# NAME OF THE PLAYER
name = input("Welcome to the Blackjack game! What is your name? ")

# CREATING THE ACCOUNT
balance = starting_money()
account = Chips(name,balance)

while True:
    
    # CREATING THE PLAYER AND THE DEALER
    player = Hand(name)
    dealer = Hand("Dealer")

    # CREATING THE DECK
    deck = Deck()
    deck.shuffle()

    # CHECKING THE BALANCE
    print(account)
    if account.balance == 0:
        print(f"{name} is out of money! Thank you for playing.")
        break
    
    # BET AND START OF THE ROUND
    bet()
    deal_cards()
    print_dealer_first()
    print_player()
    
    # PLAYER'S TURN

    players_turn = True
    while players_turn:
        hit_or_stand = input("Do you want one more card? Y/N ")
        if hit_or_stand not in ['y','Y','n','N']:
            hit_or_stand = input("Invalid input. Please enter Y or N. ")
        if hit_or_stand in ['y','Y']:
            player_hit()
            if sum(player.score) > 21:
                player_busts()
                break
        else:
            players_turn = False
    
    # DEALER'S TURN
    
    dealers_turn = True
    while dealers_turn:
        if sum(player.score) > 21:
            break
        else:
            print("\n")
            print_dealer()
            while sum(dealer.score) < 17:
                input("It's the Dealer's next turn. Press Enter to continue.")
                print("The Dealer's score is below 17. The Dealer draws another card.")
                dealer_hit()
            if sum(dealer.score) > 21:
                dealer_busts()
                break
            elif sum(player.score) >= sum(dealer.score):
                player_wins()
                break
            elif sum(player.score) < sum(dealer.score):
                player_loses()
                break

    # REPLAY?
    if not play_again():
        print("Thank you for playing! See you next time!")
        break
