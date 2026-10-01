from enum import Enum
from random import sample, randint

from config import GAMBLER_DECK_LEN, DEFAULT_TRANSFER_CARDS_DEPTH

class values_elmts(Enum):
    TWO    =  "2"
    THREE  =  "3"
    FOUR   =  "4"
    FIVE   =  "5"
    SIX    =  "6"
    SEVEN  =  "7"
    EIGHT  =  "8"
    NINE   =  "9"
    TEN    =  "10"
    GUARD  =  "guard"
    QUEEN  =  "queen"
    KING   =  "king"
    ACE    =  "ace"

class suits_elmts(Enum):
    SPADES    =  "♠"
    HEARTS    =  "♥"
    DIAMONDS  =  "♦"
    CLUBS     =  "♣"

def get_main_deck(depth=DEFAULT_TRANSFER_CARDS_DEPTH):
    suits     = set([v.value for v in suits_elmts])
    values    = set([v.value for v in values_elmts])

    fulllen   = len(suits) * len(values)
    combs     = [(v, s) for v in values for s in suits]

    res = combs
    for _ in range(depth-1):
        res = sample(res, fulllen)
    return res

def get_gamblers_decks_from(d, dlen=GAMBLER_DECK_LEN):
    deck1 = []
    deck2 = []

    start_with = [True, False][randint(0,1)]

    if start_with:
        for _ in range(dlen):
            deck1.append(d.pop())
            deck2.append(d.pop())
    else:
        for _ in range(dlen):
            deck2.append(d.pop())
            deck1.append(d.pop())

    return (deck1, deck2)


