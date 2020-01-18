import random

'''
 This are the global variables assinged to the game
 '''
suits = ('Hearts','Diamonds', 'Spades', 'Clubs')

ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Jack', 'Queen', 'King', 'Ace')

values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True

class Card:
    """
    This is the Card object being defined with its attributes
    """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    '''
    This is where we define our deck attribute containing card
    '''
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp +='\n' + card.__str__()
        return "The deck has: " + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand:
    '''
    This is where we created the hand object
    '''
    def __init__(self):
        self.cards = [ ]
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:
    '''
    This is where we create a betting object
    '''
    def __init__(self,):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    '''
    This function defines how a bet needs to be taken
    '''
    while True:
        try:
            chips.bet = int(input("How much money would you like to bet? : "))
        except ValueError:
            print('Sorry your bet needs to be an integer, please try again')
        else:
            if chips.bet > chips.total:
                print('YOU CANT BET THAT WHEN YOUR BALANCE IS ', chips.total)
            else:
                break

def hit(deck, hand):
    '''
    Here we define the func of 'HIT'
    '''
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input("Would you like to hit or stand? Enter 'h' or 's'  ")

        if x[0].lower() == 'h':
            hit(deck, hand)

        elif x[0].lower() == 's':
            print("player stands, dealer is playing")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break


def show_some(player, dealer):

    print("\nDealer's hand:")
    print(" <card is hidden> ")
    print('',dealer.cards[1])
    print("\nPlayers hand: ", *player.cards, sep= '\n ')

def show_all(player, dealer):

    print("\nDealer's hand: ", *dealer.cards, sep= '\n ' )
    print("\nDealer's hand = " , dealer.value)
    print("\nPlayer's hand: ", *player.cards, sep= '\n ')
    print("\nPlayer's hand = ", player.value)

def player_busts(player,dealer,chips):
    print("Player has lost the game")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Congradulations, you won!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("Dealer has lost the game")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("Dealer has won!")
    chips.lose_bet()

def push(player,dealer):
    print("player and dealer are tie! its a push")

while True:

    print("Welcome to Black Jack, get as close to 21 as you can \nDealer will hit untill he reaches 17, Aces count as 1 or 11")

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    player_chips = Chips()

    take_bet(player_chips)

    show_some(player_hand, dealer_hand)

    while playing:

        hit_or_stand(deck, player_hand)

        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break


    if player_hand.value <= 21:

        while dealer_hand.value <= 17:
            hit(deck, dealer_hand)

        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)

        else:
            push(player_hand, dealer_hand)

    print("\nPlayer's winnings stand at a total of ", player_chips.total)

    new_game = input("DO YOU WANT TO PLAY AGAIN???")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thanks for playing!")

