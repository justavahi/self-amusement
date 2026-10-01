from deck import values_elmts
from config import SUPERIOR_SUIT_BONUS, SEPARATOR_SYM, SEPARATOR_LENGTH

priots = {
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

def calc_card_val(card, supsuit, bonus=SUPERIOR_SUIT_BONUS):
    res         = priots[card[0]]
    if card[1] == supsuit:
        res += bonus
    return res


def bot_answer(botdeck, usrcard, supsuit):
    res = None
    usrcard_val = calc_card_val(usrcard, supsuit)

    for botcard in botdeck:
        botcard_val = calc_card_val(botcard, supsuit)

        # must be able to beat the user's card
        if botcard_val <= usrcard_val:
            continue

        # must follow suit, unless playing a trump
        if botcard[1] != usrcard[1] and botcard[1] != supsuit:
            continue

        if res is None:
            res = botcard
            continue

        # prefer lower-value winning card (classic strategy)
        if calc_card_val(botcard, supsuit) < calc_card_val(res, supsuit):
            res = botcard

    return res

# test
def demonstrate_bot_answer(usrdeck, botdeck, superior_suit, sepsym=SEPARATOR_SYM, seplen=SEPARATOR_LENGTH):
    print(f"user deck\t\t{usrdeck}")
    print(f"bot  deck\t\t{botdeck}")
    print()

    print(f"superior\t\t{superior_suit}\n")
    for card in usrdeck:
        ans = bot_answer(botdeck, card, superior_suit)

        print(f"{sepsym * seplen}")
        print(f"user card\t\t{card}")
        print(f"bot deck\t\t{botdeck}")
        print(f"bot's solution\t\t{ans}")
        print(f"{sepsym * seplen}")
        print()

def game(main_deck, usrdeck, botdeck):
    superior_suit = main_deck[0][1]
    demonstrate_bot_answer(usrdeck, botdeck, superior_suit)
