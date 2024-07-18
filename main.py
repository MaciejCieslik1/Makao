from screens import beginning_screen, choose_number_of_opponents_screen, choose_difficulty_screen
from game import Game


def main():
    """Main program. Call all screens in correct order."""
    while True:
        beginning_screen()
        number_of_opponents = choose_number_of_opponents_screen()
        difficulty = choose_difficulty_screen()
        game = Game(number_of_opponents + 1, difficulty)
        game.game_loop()


if __name__ == "__main__":
    main()
