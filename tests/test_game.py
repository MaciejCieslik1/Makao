from cards import Card, create_cards
from play_service import PlayService
from game import Game
from players import Player
from cards_piles import CardOnField, CardsPile, BinCardsPile


def test_create_players_list():
    game = Game(4, True)
    cards = create_cards()
    cards_pile = CardsPile(cards)
    bin_cards_pile = BinCardsPile()
    game.create_players_list(4, cards_pile, bin_cards_pile)
    assert len(game.list_of_players) == 4


def test_game_create():
    game = Game(4, True)
    assert game.number_of_players == 4
    assert game.players_who_finished == []
    assert game.current_player is None
    assert game.list_of_players == []
    assert game.end_turn is False
    assert game.human_in_game is True
    assert game.out_of_cards is False


def test_game_make_playable_list():
    game = Game(4, True)
    play_service = PlayService()
    card_on_field = CardOnField(Card("5", "diamond", "path"))
    cards = [Card("5", "heart", "path"), Card("J", "diamond", "path")]
    player = Player(cards, "player")
    game.current_player = player
    playable_list = game.make_playable_list(card_on_field, play_service)
    assert len(playable_list) == 2


def test_game_make_playable_list_protective_card():
    game = Game(4, True)
    play_service = PlayService()
    card_on_field = CardOnField(Card("5", "diamond", "path"))
    play_service.protective_card = Card("5", "spade", "path")
    playable_list = game.make_playable_list(card_on_field, play_service)
    assert len(playable_list) == 1
    assert playable_list[0].number == "5"
    assert playable_list[0].color == "spade"
    assert playable_list[0].image == "path"


def test_game_make_playable_list_protective_card_no_protection():
    game = Game(4, True)
    play_service = PlayService()
    card_on_field = CardOnField(Card("5", "diamond", "path"))
    play_service.protective_card = Card("7", "spade", "path")
    playable_list = game.make_playable_list(card_on_field, play_service)
    assert len(playable_list) == 0
    assert playable_list == []


def test_game_make_playable_list_1_card():
    game = Game(4, True)
    play_service = PlayService()
    card_on_field = CardOnField(Card("A", "heart", "path"))
    cards = [Card("Q", "heart", "path")]
    player = Player(cards, "player")
    game.current_player = player
    playable_list = game.make_playable_list(card_on_field, play_service)
    assert len(playable_list) == 1


def test_make_same_numbers_list():
    game = Game(4, True)
    card_on_field = CardOnField(Card("A", "heart", "path"))
    cards = [Card("A", "spade", "path"), Card("A", "diamond", "path"), Card("A", "club", "path")]
    player = Player(cards, "player")
    game.current_player = player
    same_numbers_list = game.make_same_numbers_list(card_on_field)
    assert len(same_numbers_list) == 3


def test_create_players_list_2():
    game = Game(2, False)
    cards = create_cards()
    cards_pile = CardsPile(cards)
    bin_cards_pile = BinCardsPile()
    game.create_players_list(2, cards_pile, bin_cards_pile)
    assert len(game.list_of_players) == 2
    assert game.number_of_players == 2


def test_create_players_list_3():
    game = Game(3, True)
    cards = create_cards()
    cards_pile = CardsPile(cards)
    bin_cards_pile = BinCardsPile()
    game.create_players_list(3, cards_pile, bin_cards_pile)
    assert len(game.list_of_players) == 3
    assert game.number_of_players == 3


def test_create_players_list_4():
    game = Game(4, True)
    cards = create_cards()
    cards_pile = CardsPile(cards)
    bin_cards_pile = BinCardsPile()
    game.create_players_list(4, cards_pile, bin_cards_pile)
    assert len(game.list_of_players) == 4
    assert game.number_of_players == 4
