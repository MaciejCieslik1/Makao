import pygame
from buttons import Button, draw_player_cards, draw_card_on_table, draw_text, draw_control_buttons, draw_all_opponents
from cards import Card
from enum import Enum


pygame.init()
WIDTH, HEIGHT = 1800, 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = "images/background.png"
FPS = 60
pygame.display.set_caption("Makao")


background_image = pygame.image.load("images/background.png").convert()
scaled_background = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


class DemandName(Enum):
    DEMAND_NOTHING = "nothing"


def beginning_screen():
    """Draw beggining screen with play and exit buttons."""
    run = True
    clock = pygame.time.Clock()
    play_button = Button(700, 450, 150, 100, (245, 132, 66), "PLAY", 60)
    exit_button = Button(950, 450, 150, 100, (245, 132, 66), "EXIT", 60)
    while run:
        clock.tick(FPS)
        SCREEN.blit(scaled_background, (0, 0))
        if play_button.draw(SCREEN):
            run = False
        elif exit_button.draw(SCREEN):
            pygame.quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()


def choose_number_of_opponents_screen():
    """Draw screen which allows player to choose number of opponents.

    Return:
    Number of opponents chosen by player.
    """
    run = True
    clock = pygame.time.Clock()
    one_button = Button(600, 450, 100, 100, (245, 132, 66), "1", 60)
    two_button = Button(850, 450, 100, 100, (245, 132, 66), "2", 60)
    three_button = Button(1100, 450, 100, 100, (245, 132, 66), "3", 60)
    while run:
        clock.tick(FPS)
        SCREEN.blit(scaled_background, (0, 0))
        draw_text("Select number of opponents", 900, 300, 80, SCREEN)
        if one_button.draw(SCREEN):
            number_of_opponents = 1
            run = False
        elif two_button.draw(SCREEN):
            number_of_opponents = 2
            run = False
        elif three_button.draw(SCREEN):
            number_of_opponents = 3
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
    return number_of_opponents


def choose_difficulty_screen():
    """Draw screen which allows player to choose difficulty level(easy or hard).

    Return:
    Difficult variable which is true when chosen difficuty is hard or false, when chosen difficulty is easy.
    """
    run = True
    clock = pygame.time.Clock()
    easy_button = Button(700, 450, 150, 100, (245, 132, 66), "EASY", 60)
    hard_button = Button(950, 450, 150, 100, (245, 132, 66), "HARD", 60)
    while run:
        clock.tick(FPS)
        SCREEN.blit(scaled_background, (0, 0))
        draw_text("Select difficulty level", 900, 300, 80, SCREEN)
        if easy_button.draw(SCREEN):
            difficult = False
            run = False
        if hard_button.draw(SCREEN):
            difficult = True
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
    return difficult


def jack_demand_screen():
    """Draw screen which allows player to choose number demanded by jack card.

    Return:
    Demand, which is card with number attribute equal to chosen demand number.
    """
    run = True
    clock = pygame.time.Clock()
    five_button = Button(700, 300, 100, 100, (245, 132, 66), "5", 60)
    six_button = Button(850, 300, 100, 100, (245, 132, 66), "6", 60)
    seven_button = Button(1000, 300, 100, 100, (245, 132, 66), "7", 60)
    eight_button = Button(700, 450, 100, 100, (245, 132, 66), "8", 60)
    nine_button = Button(850, 450, 100, 100, (245, 132, 66), "9", 60)
    ten_button = Button(1000, 450, 100, 100, (245, 132, 66), "10", 60)
    nothing_button = Button(800, 600, 200, 100, (245, 132, 66), "nothing", 60)
    while run:
        clock.tick(FPS)
        SCREEN.blit(scaled_background, (0, 0))
        draw_text("Select demand", 900, 200, 80, SCREEN)
        if five_button.draw(SCREEN):
            demand = Card("5", "diamond", "path")
            run = False
        elif six_button.draw(SCREEN):
            demand = Card("6", "diamond", "path")
            run = False
        elif seven_button.draw(SCREEN):
            demand = Card("7", "diamond", "path")
            run = False
        elif eight_button.draw(SCREEN):
            demand = Card("8", "diamond", "path")
            run = False
        elif nine_button.draw(SCREEN):
            demand = Card("9", "diamond", "path")
            run = False
        elif ten_button.draw(SCREEN):
            demand = Card("10", "diamond", "path")
            run = False
        elif nothing_button.draw(SCREEN):
            demand = "nothing"
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
    return demand


def ace_demand_screen():
    """Draw screen which allows player to choose color demanded by ace card.

    Return:
    Demand, which is card with color attribute equal to chosen demand color.
    """
    run = True
    clock = pygame.time.Clock()
    heart_button = Button(675, 300, 200, 100, (245, 132, 66), "heart", 60)
    diamond_button = Button(925, 300, 200, 100, (245, 132, 66), "diamond", 60)
    spade_button = Button(675, 450, 200, 100, (245, 132, 66), "spade", 60)
    club_button = Button(925, 450, 200, 100, (245, 132, 66), "club", 60)
    nothing_button = Button(800, 600, 200, 100, (245, 132, 66), "nothing", 60)
    while run:
        clock.tick(FPS)
        SCREEN.blit(scaled_background, (0, 0))
        draw_text("Select demand", 900, 200, 80, SCREEN)
        if heart_button.draw(SCREEN):
            demand = Card("5", "heart", "path")
            run = False
        elif diamond_button.draw(SCREEN):
            demand = Card("5", "diamond", "path")
            run = False
        elif spade_button.draw(SCREEN):
            demand = Card("5", "spade", "path")
            run = False
        elif club_button.draw(SCREEN):
            demand = Card("5", "club", "path")
            run = False
        elif nothing_button.draw(SCREEN):
            demand = "nothing"
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
    return demand


def results_screen(players_who_finished):
    """Draw screen which displays results list.

    Arguments:
    players_who_finished -- list of players who finished the game
    """
    run = True
    clock = pygame.time.Clock()
    main_menu_button = Button(800, 400 + 50 * len(players_who_finished), 200, 100, (245, 132, 66), "MENU", 60)
    while run:
        clock.tick(FPS)
        SCREEN.blit(scaled_background, (0, 0))
        draw_text("Results list", 900, 200, 80, SCREEN)
        for number, participant in enumerate(players_who_finished):
            line = f"{number + 1 }. {participant.name}"
            draw_text(line, 900, 300 + 50 * number, 50, SCREEN)
        if main_menu_button.draw(SCREEN):
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()


def out_of_cards_screen():
    """Draw screen which displays communicate, when all cards have run out."""
    run = True
    clock = pygame.time.Clock()
    main_menu_button = Button(800, 600, 200, 100, (245, 132, 66), "MENU", 60)
    while run:
        clock.tick(FPS)
        SCREEN.blit(scaled_background, (0, 0))
        draw_text("Out of cards", 900, 400, 100, SCREEN)
        if main_menu_button.draw(SCREEN):
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()


def game_loop_screen(list_of_players, card_on_field, play_service):
    """Draw screen which displays current game state.

    Arguments:
    list_of_players -- list of players who still have cards
    card_on_field -- card in the centre of the table
    play_service -- object which determines current game parameters

    Return:
    Chosen card object, if player chose card. Else chosen command.
    """
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        SCREEN.blit(scaled_background, (0, 0))
        draw_all_opponents(list_of_players, SCREEN)
        draw_card_on_table(card_on_field, 831, 395, SCREEN)
        for participant in list_of_players:
            if participant.name == "player":
                player = participant
        chosen_card = draw_player_cards(player, SCREEN)
        if chosen_card:
            run = False
        chosen_command = draw_control_buttons(SCREEN)
        if chosen_command:
            run = False
        if play_service.jack_demand:
            demand_text = f"demand: {play_service.jack_demand.number}"
            draw_text(demand_text, 700, 475, 40, SCREEN)
            counter_text = f"turns left: {play_service.jack_counter}"
            draw_text(counter_text, 700, 525, 40, SCREEN)
        elif play_service.ace_demand:
            demand_text = f"demand: {play_service.ace_demand.color}"
            draw_text(demand_text, 700, 475, 40, SCREEN)
        elif play_service.attack_value:
            demand_text = f"attack: {play_service.attack_value}"
            draw_text(demand_text, 1075, 475, 40, SCREEN)
        elif play_service.four_counter:
            demand_text = f"four counter: {play_service.four_counter}"
            draw_text(demand_text, 1075, 525, 40, SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
    if chosen_card:
        return chosen_card
    return chosen_command
