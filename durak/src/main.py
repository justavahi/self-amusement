from deck import get_main_deck, get_gamblers_decks_from
from game import game

main_deck         = get_main_deck(10)
usrdeck, botdeck  = get_gamblers_decks_from(main_deck)

if __name__ == "__main__":
    game()
