from config import SEPARATOR_SYM, SEPARATOR_LENGTH

def print_card(card, sep='\n'):
    val, suit = card
    print(f"{val}{suit}", end=sep)

def print_deck(deck, sep='\n', greeting='\n'):
    print(greeting, end='')
    for card in deck:
        print_card(card, ' ')
    print(sep, end="")

def print_desktop(desktop, sep='\n'):
    if len(desktop) > 0:
        print(SEPARATOR_SYM * 10, "Desktop entry", SEPARATOR_SYM * 10)

        for pair in desktop:
            attack_card, defense_card = pair

            print(f"Attack card\t", end='')
            print_card(attack_card)

            print(f"Defense card\t", end='')
            print_card(defense_card)

        print(sep, end='')
    else:
        print("Empty desktop", end=sep)

def print_info(desktop, usrdeck, superior_suit, isUsrQueue):
    print_desktop(desktop)
    print(f"Superior suit\t{superior_suit}")
    print_deck(usrdeck, greeting="Your deck\t")

