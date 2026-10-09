from enum import Enum
from random import sample, randint

from config import GAMBLER_DECK_LEN, DEFAULT_TRANSFER_CARDS_DEPTH, SUPERIOR_SUIT_BONUS 

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

PRIOTS = {
        values_elmts.TWO.value:    2,
        values_elmts.THREE.value:  3,
        values_elmts.FOUR.value:   4,
        values_elmts.FIVE.value:   5,
        values_elmts.SIX.value:    6,
        values_elmts.SEVEN.value:  7,
        values_elmts.EIGHT.value:  8,
        values_elmts.NINE.value:   9,
        values_elmts.TEN.value:    10,

        values_elmts.GUARD.value:  11,
        values_elmts.QUEEN.value:  12,
        values_elmts.KING.value:   13,
        values_elmts.ACE.value:    14,
}

# O(1)
def calc_card_val(card, supsuit, bonus=SUPERIOR_SUIT_BONUS): 
    res         = PRIOTS[card[0]]
    if card[1] == supsuit:
        res += bonus
    return res

# O(nlogn)
def sort_deck(deck, supsuit):
    suits = [v.value for v in suits_elmts] 
    for i in range(len(suits)):
        if suits[i] == supsuit:
            suits[0], suits[i] = suits[i], suits[0]
            break

    n = len(deck)
    res = []

    for suit in suits:
        cards_of_one_suit = []
        
        for i in range(n):
            v, s = deck[i]
            if s == suit:
                card = (deck[i], calc_card_val(deck[i], supsuit)) 
                cards_of_one_suit.append(card)
        cards_of_one_suit.sort(key=lambda x: x[1])

        for card in cards_of_one_suit:
            res.append(card[0])

    for i in range(n):
        deck[i] = res[i]
