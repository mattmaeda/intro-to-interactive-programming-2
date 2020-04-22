# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
TITLE_POS = (50, 50)
DEALER_SCORE_POS = (50, 80)
PLAYER_SCORE_POS = (50, 100)
MESSAGE_POS = (50, 140)
DEALER_TEXT_POS = (50, 180)
DEALER_HAND_YPOS = 200
PLAYER_TEXT_POS = (50, 380)
PLAYER_HAND_YPOS = 400

in_play = False
outcome = ""
dealer_score = 0
player_score = 0
message = "Hit or Stand?"
deck = None
player = None
dealer = None

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self, is_dealer=False):
        self.cards = []
        self.is_dealer = is_dealer

    def __str__(self):
        pass	# return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        values = [VALUES.get(card.get_rank()) for card in self.cards]

        if 1 in values and sum(values) <= 11:
            return sum(values) + 10
        else:
            return sum(values)

    def draw(self, canvas, y_axis, in_play):
        x_axis = 50

        for card in self.cards:
            pos = (x_axis, y_axis)

            # Draw covered card
            if self.is_dealer and x_axis == 50 and in_play:
                canvas.draw_image(
                    card_back,
                    CARD_BACK_CENTER,
                    CARD_BACK_SIZE,
                    [
                        x_axis + CARD_BACK_CENTER[0],
                        y_axis + CARD_BACK_CENTER[1]
                    ],
                    CARD_BACK_SIZE
                )
            else:
                card.draw(canvas, pos)

            x_axis += 72


# define deck class
class Deck:
    def __init__(self):
        self.cards = [Card(s, r) for r in RANKS for s in SUITS]
        self.shuffle()

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()

    def __str__(self):
        for card in self.cards:
            print card


#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, deck
    global dealer_score
    global message

    if in_play:
        message = "Dealer wins.  Hit or stand?"
        dealer_score += 1

    # your code goes here
    deck = Deck()
    player = Hand()
    dealer = Hand(True)
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())

    in_play = True

def hit():
    global player, dealer, in_play
    global deck, player_score, dealer_score
    global message

    # if the hand is in play, hit the player
    if in_play:
        player.add_card(deck.deal_card())

        # if busted, assign a message to outcome, update in_play and score
        if player.get_value() > 21:
            message = "You busted.  Dealer wins. New deal?"
            dealer_score += 1
            in_play = False


def stand():
    global in_play, dealer, player
    global player_score, dealer_score
    global message

    in_play = False

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while dealer.get_value() < 17:
        dealer.add_card(deck.deal_card())

    if dealer.get_value() > 21:
        message = "Dealer busted.  You win.  New deal?"
        player_score += 1
    elif dealer.get_value() == player.get_value():
        message = "Tie.  New deal?"
    elif dealer.get_value() > player.get_value():
        message = "Dealer wins.  New deal?"
        dealer_score += 1
    else:
        message = "You win.  New deal?"
        player_score += 1


# draw handler
def draw(canvas):
    global player, dealer, in_play
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", TITLE_POS, 45, "Pink")
    canvas.draw_text("Dealer Wins: %d" % dealer_score, DEALER_SCORE_POS, 20, "Black")
    canvas.draw_text("Player Wins: %d" % player_score, PLAYER_SCORE_POS, 20, "Black")
    canvas.draw_text(message, MESSAGE_POS, 20, "White")
    canvas.draw_text("Dealer Hand", DEALER_TEXT_POS, 20, "Black")
    canvas.draw_text("Player Hand", PLAYER_TEXT_POS, 20, "Black")

    # Draw dealer cards
    dealer.draw(canvas, DEALER_HAND_YPOS, in_play)

    # Draw player cards
    player.draw(canvas, PLAYER_HAND_YPOS, in_play)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
