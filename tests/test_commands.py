from commands import Command
from cards import Card
from play_service import PlayService
from game import Game
from players import Player


def test_create_commands():
    command = Command("makao")
    assert command.name == "makao"


def test_command_has_name():
    command = Command("stop makao")
    assert command.has_name("stop makao")


def test_is_enable_not_makao():
    command = Command("makao")
    play_service = PlayService()
    game = Game(4, True)
    cards = [Card("6", "heart", "path"), Card("5", "spade", "path")]
    player = Player(cards, "player")
    game.current_player = player
    assert not command.is_enable(play_service, game)


# def test_is_enable_makao():
#     command = Command("makao")
#     play_service = PlayService()
#     game = Game(4, True)
#     cards = [Card("6", "heart", "path")]
#     player = Player(cards, "player")
#     game.current_player = player
#     game.current_player.has_makao = True
#     assert command.is_enable(play_service, game)


# def test_is_enable_not_stop_makao_not_said_makao():
#     command = Command("stop makao")
#     play_service = PlayService()
#     game = Game(4, True)
#     cards = [Card("6", "heart", "path")]
#     player = Player(cards, "player")
#     game.current_player = player
#     game.current_player.has_makao = True
#     assert command.is_enable(play_service, game)


def test_is_enable_not_stop_makao_said_makao():
    command = Command("stop makao")
    play_service = PlayService()
    game = Game(4, False)
    cards = [Card("6", "heart", "path")]
    player = Player(cards, "player")
    game.current_player = player
    game.current_player.has_makao = True
    game.current_player.said_makao = True
    assert not command.is_enable(play_service, game)


def test_is_enable_end_turn_no_protective_card_no_card_was_played():
    command = Command("end turn")
    play_service = PlayService()
    game = Game(4, False)
    assert not command.is_enable(play_service, game)


def test_is_enable_end_turn_card_was_played():
    command = Command("end turn")
    play_service = PlayService()
    game = Game(4, False)
    play_service.card_was_played = True
    assert command.is_enable(play_service, game)


def test_is_enable_end_turn_four_counter():
    command = Command("end turn")
    play_service = PlayService()
    game = Game(4, True)
    play_service.four_counter = 1
    assert command.is_enable(play_service, game)


def test_is_enable_end_turn_protective_card_no_attack():
    command = Command("end turn")
    play_service = PlayService()
    game = Game(4, True)
    play_service.protective_card = Card("K", "diamond", "path")
    assert command.is_enable(play_service, game)


def test_is_enable_end_turn_protective_card_attack():
    command = Command("end turn")
    play_service = PlayService()
    game = Game(4, False)
    play_service.protective_card = Card("K", "diamond", "path")
    play_service.attack_value = 1
    assert not command.is_enable(play_service, game)


def test_is_enable_end_turn_no_protective_card():
    command = Command("end turn")
    play_service = PlayService()
    game = Game(4, True)
    assert not command.is_enable(play_service, game)


def test_is_enable_end_turn_no_protective_card_attack():
    command = Command("end turn")
    play_service = PlayService()
    game = Game(4, True)
    play_service.attack_value = 1
    assert not command.is_enable(play_service, game)
