# implementation of card game - Memory

import simplegui
import random
import time

# Globals
DECK = []
SELECTED = []
RECT_WIDTH = 50
RECT_HEIGHT = 100
TURNS = 0

# helper function to initialize globals
def new_game():
    global DECK, TURNS, SELECTED
    DECK = []
    SELECTED = []
    TURNS = 0

    for i in range(1, 9):
        DECK.append({
                "value": i,
                "exposed": False
                })
        DECK.append({
                "value": i,
                "exposed": False
                })

    random.shuffle(DECK)
    label.set_text("Turns = %d" % TURNS)

def wait(seconds):
    """
    Wait during `seconds` seconds.

    :param seconds: (int or float) >= 0
    """
    assert isinstance(seconds, int) or isinstance(seconds, float), \
        type(seconds)

    start = time.time()
    while time.time() - start < seconds:
        pass

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global SELECTED, TURNS

    idx = pos[0] // 50
    card = DECK[idx]

    if not card.get("exposed"):
        card["exposed"] = True

        if len(SELECTED) == 2:
            if SELECTED[0].get("value") != SELECTED[1].get("value"):
                SELECTED[0]["exposed"] = False
                SELECTED[1]["exposed"] = False

            TURNS += 1
            label.set_text("Turns = %d" % TURNS)
            SELECTED = []

        SELECTED.append(card)


# cards are logically 50x100 pixels in size
def draw(canvas):
    global TURNS

    rect_left = 0
    rect_top = 0
    rect_bottom = rect_top + RECT_HEIGHT
    selected = []

    for card in DECK:
        rect_right = rect_left + RECT_WIDTH

        canvas.draw_polygon(
            [
                (rect_left, rect_top),
                (rect_right, rect_top),
                (rect_right, rect_bottom),
                (rect_left, rect_bottom)
            ],
            5,
            "Green",
            "White"
        )

        if card.get("exposed"):
            canvas.draw_text(
                str(card.get("value")),
                (rect_left + 25, rect_top + 50),
                24,
                "Green"
            )

        rect_left += RECT_WIDTH


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubrice
