from random import choice

from deck import calc_card_val, sort_deck
from config import SEPARATOR_SYM, SEPARATOR_LENGTH
from output import print_card, print_deck, print_desktop, print_info

def bot_defense(botdeck, usrcard, supsuit):
    res_card, res_id = None, None
    usrcard_val = calc_card_val(usrcard, supsuit)

    for i in range(len(botdeck)):
        botcard = botdeck[i]
        botcard_val = calc_card_val(botcard, supsuit)

        # must be able to beat the user's card
        if botcard_val <= usrcard_val:
            continue

        # must follow suit, unless playing a trump
        if botcard[1] != usrcard[1] and botcard[1] != supsuit:
            continue

        if res_card is None:
            res_card = botcard
            res_id   = i
            continue

        # prefer lower-value winning card (classic strategy)
        if calc_card_val(botcard, supsuit) < calc_card_val(res_card, supsuit):
            res_card = botcard
            res_id   = i

    return (res_card, res_id)

def bot_attack(botdeck: [(str, str)], supsuit: str) -> ([(str, str)], int): # calculating the average val
    if not botdeck:
        return None

    vals = [(x, calc_card_val(x, supsuit)) for x in botdeck]
    vals.sort(key=lambda x: x[1])

    av = sum(x for _, x in vals) // len(vals)

    res_id = 0
    while av - vals[res_id][1] > 0:
        res_id += 1

    res = vals[res_id-1][0]
    return (res, botdeck.index(res))

def is_valid_to_defend(defend_card: [(str, str)], attack_card: [(str, str)], supsuit: str) -> bool:
    dval, aval = calc_card_val(defend_card, supsuit), calc_card_val(attack_card, supsuit)
    check_val  = (dval > aval)

    dsuit, asuit = defend_card[1], attack_card[1]
    check_suit = (dsuit == supsuit or dsuit == asuit)

    return check_val and check_suit

# test
def demonstrate_bot_answer(usrdeck, botdeck, superior_suit, sepsym=SEPARATOR_SYM, seplen=SEPARATOR_LENGTH):
    print(f"user deck\t\t{usrdeck}")
    print(f"bot  deck\t\t{botdeck}")
    print()

    print(f"superior\t\t{superior_suit}\n")
    for card in usrdeck:
        ans, i = bot_defense(botdeck, card, superior_suit)

        print(f"{sepsym * seplen}")
        print(f"user card\t\t{card}")
        print(f"bot deck\t\t{botdeck}")
        print(f"bot's solution\t\t{ans} ( {i+1} card in desk )")
        print(f"{sepsym * seplen}")
        print()

# Game!!!
def erase_from_deck(deck, id, supsuit):
    deck[-1], deck[id] = deck[id], deck[-1]
    return deck.pop()

def claim_desktop(gamblerdeck, desktop):
    for pair in desktop:
        attack_card, defense_card = pair

        if attack_card:
            gamblerdeck.append(attack_card)
        if defense_card:
            gamblerdeck.append(defense_card)

def fill_deck(main_deck, gamblerdeck, necessary_len):
    n = len(gamblerdeck)
    while n < necessary_len and main_deck:
        gamblerdeck.append(main_deck.pop())
        n += 1

"""
We don't store used cards(for now we can use any card in the move)
TODO: 
    1) fix it!
    2) finish with user defense stuff
"""
def move(main_deck, usrdeck, botdeck, superior_suit, isUsrQueue):
    desktop = set()

    if isUsrQueue:
        print("You may attack")
        while usrdeck and botdeck:
            inp = input("Please select what card to use by id(1-6/d): ")
            if inp == "d":
                break

            id = int(inp) - 1
            usrcard = erase_from_deck(usrdeck, id, superior_suit)
            sort_deck(usrdeck, superior_suit)
            print()

            botcard, botcard_id = bot_defense(botdeck, usrcard, superior_suit)
            if not botcard:
                print("Bot claims cards from the desktop")
                claim_desktop(botdeck, desktop)
                return False

            desktop.add( (usrcard, botcard) )
            erase_from_deck(botdeck, botcard_id, superior_suit)

            print_info(desktop, usrdeck, superior_suit, isUsrQueue)
    else:
        botcard, botcard_id = bot_attack(botdeck, superior_suit)
        erase_from_deck(botdeck, botcard_id, superior_suit)

        print(f"Bot used {botcard}")
        desktop.add( (botcard, None) )
        print_info(desktop, usrdeck, superior_suit, isUsrQueue)
        
        print("You may defend")
        while usrdeck and botdeck:
            inp = input("Please select what card to use by id(1-6/c): ")
            if inp == "c":
                claim_desktop(usrdeck, desktop)
                return False
            
            id = int(inp) - 1
            usrcard = usrdeck[id]
            
            if not is_valid_to_defend(usrcard, botcard, superior_suit):
                print("Not a valid card to defend. Choose again")
                continue

            erase_from_deck(usrdeck, id, superior_suit)
            sort_deck(usrdeck, superior_suit)
            print()

            desktop.pop() # delete not full pair to fill again with a full one
            desktop.add( (botcard, usrcard) )
            
            botcard, botcard_id = bot_attack(botdeck, superior_suit)

            desktop.add( (usrcard, botcard) )
            erase_from_deck(botdeck, botcard_id, superior_suit)

            botcard, botcard_id = bot_attack(botdeck, superior_suit)
            erase_from_deck(botdeck, botcard_id, superior_suit)

    return True

def game(main_deck, usrdeck, botdeck):
    isUsrQueue = False #choice([True, False])

    # Pre-Last Cards
    print(f"Superior suit\t{main_deck[0][1]}")
    print_deck(usrdeck, greeting="Your deck\t")
    print_deck(botdeck, greeting="Bot deck\t", sep="\n\n")

    while main_deck:
        was_not_took = move(main_deck, usrdeck, botdeck, main_deck[0][1], isUsrQueue)

        print("Refilling gamblers decks")
        fill_deck(main_deck, usrdeck, 6)
        fill_deck(main_deck, botdeck, 6)

        if was_not_took:
            isUsrQueue = not isUsrQueue

