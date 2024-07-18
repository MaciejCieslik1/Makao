from cards import create_cards, Card
from play_service import PlayService
from cards_piles import CardsPile, BinCardsPile, CardOnField
from game import Game
from commands import Command
from players import Player


def test_play_service_create():
    play_service = PlayService()
    assert play_service.jack_demand is None
    assert play_service.jack_counter == 0
    assert play_service.ace_demand is None
    assert play_service.attack_value == 0
    assert play_service.four_counter == 0
    assert play_service.changed_order is False
    assert play_service.active_king_played is False
    assert play_service.protective_card is None
    assert play_service.card_was_played is False


def test_play_card_2():
    card_on_table = Card("7", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    bin_cards_pile = BinCardsPile([])
    play_service = PlayService()
    card = Card("2", "heart", "path")
    game = Game(4, True)
    demand = None
    cards = [card]
    player = Player(cards, "player")
    game.current_player = player
    play_service.play_card(card, demand, game, card_on_field, bin_cards_pile)
    assert play_service.attack_value == 2
    assert play_service.card_was_played is True


def test_play_card_3():
    play_service = PlayService()
    card_on_table = Card("7", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    bin_cards_pile = BinCardsPile([])
    card = Card("3", "heart", "path")
    game = Game(4, True)
    demand = None
    cards = [Card("6", "heart", "path"), card]
    player = Player(cards, "player")
    game.current_player = player
    play_service.play_card(card, demand, game, card_on_field, bin_cards_pile)
    assert play_service.attack_value == 3
    assert play_service.card_was_played is True


def test_play_card_3_default_attack_value_2():
    card_on_table = Card("7", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    bin_cards_pile = BinCardsPile([])
    play_service = PlayService()
    card = Card("3", "heart", "path")
    game = Game(4, False)
    play_service.attack_value = 2
    demand = None
    cards = [Card("6", "heart", "path"), card]
    player = Player(cards, "player")
    game.current_player = player
    play_service.play_card(card, demand, game, card_on_field, bin_cards_pile)
    assert play_service.attack_value == 5
    assert play_service.card_was_played is True


def test_play_card_4_default_four_counter_2():
    card_on_table = Card("7", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    bin_cards_pile = BinCardsPile([])
    play_service = PlayService()
    card = Card("4", "heart", "path")
    game = Game(4, True)
    play_service.four_counter = 2
    demand = None
    cards = [Card("6", "heart", "path"), card]
    player = Player(cards, "player")
    game.current_player = player
    play_service.play_card(card, demand, game, card_on_field, bin_cards_pile)
    assert play_service.four_counter == 3
    assert play_service.card_was_played is True


def test_play_card_king_heart_default_attack_value_2():
    card_on_table = Card("7", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    bin_cards_pile = BinCardsPile([])
    play_service = PlayService()
    card = Card("K", "heart", "path")
    game = Game(4, True)
    play_service.attack_value = 2
    demand = None
    cards = [Card("6", "heart", "path"), card]
    player = Player(cards, "player")
    game.current_player = player
    play_service.play_card(card, demand, game, card_on_field, bin_cards_pile)
    assert play_service.attack_value == 7
    assert play_service.active_king_played is True
    assert play_service.card_was_played is True


def test_play_card_king_spade_default_attack_value_2():
    card_on_table = Card("7", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    bin_cards_pile = BinCardsPile([])
    play_service = PlayService()
    card = Card("K", "spade", "path")
    game = Game(4, False)
    play_service.attack_value = 2
    demand = None
    cards = [Card("6", "heart", "path"), card]
    player = Player(cards, "player")
    game.current_player = player
    play_service.play_card(card, demand, game, card_on_field, bin_cards_pile)
    assert play_service.attack_value == 7
    assert play_service.active_king_played is True
    assert play_service.changed_order is True
    assert play_service.card_was_played is True


def test_play_card_king_diamond_default_attack_value_2():
    card_on_table = Card("7", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    bin_cards_pile = BinCardsPile([])
    play_service = PlayService()
    card = Card("K", "diamond", "path")
    game = Game(4, True)
    play_service.attack_value = 5
    demand = None
    cards = [Card("6", "heart", "path"), card]
    player = Player(cards, "player")
    game.current_player = player
    play_service.play_card(card, demand, game, card_on_field, bin_cards_pile)
    assert play_service.attack_value == 0
    assert play_service.active_king_played is False
    assert play_service.changed_order is False
    assert play_service.card_was_played is True


def test_play_card_king_club_default_attack_value_2():
    card_on_table = Card("7", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    bin_cards_pile = BinCardsPile([])
    play_service = PlayService()
    card = Card("K", "club", "path")
    game = Game(4, True)
    play_service.attack_value = 5
    demand = None
    cards = [Card("6", "heart", "path"), card]
    player = Player(cards, "player")
    game.current_player = player
    play_service.play_card(card, demand, game, card_on_field, bin_cards_pile)
    assert play_service.attack_value == 0
    assert play_service.active_king_played is False
    assert play_service.changed_order is False
    assert play_service.card_was_played is True


def test_play_card_jack_diamond_demand_5_2_cards():
    card_on_table = Card("7", "diamond", "path")
    card_on_field = CardOnField(card_on_table)
    bin_cards_pile = BinCardsPile([])
    play_service = PlayService()
    card = Card("J", "diamond", "path")
    game = Game(4, False)
    demand = Card("5", "diamond", "path")
    cards = [Card("6", "heart", "path"), card]
    player = Player(cards, "player")
    game.current_player = player
    play_service.play_card(card, demand, game, card_on_field, bin_cards_pile)
    assert play_service.jack_demand.number == demand.number
    assert play_service.jack_counter == 5
    assert play_service.card_was_played is True


def test_play_card_jack_diamond_demand_5_1_card():
    card_on_table = Card("7", "diamond", "path")
    card_on_field = CardOnField(card_on_table)
    bin_cards_pile = BinCardsPile([])
    play_service = PlayService()
    card = Card("J", "diamond", "path")
    game = Game(4, True)
    demand = Card("5", "diamond", "path")
    cards = [card]
    player = Player(cards, "player")
    game.current_player = player
    play_service.play_card(card, demand, game, card_on_field, bin_cards_pile)
    assert play_service.jack_demand.number == demand.number
    assert play_service.jack_counter == 4
    assert play_service.card_was_played is True


def test_play_card_ace_diamond_demand_heart():
    card_on_table = Card("7", "diamond", "path")
    card_on_field = CardOnField(card_on_table)
    bin_cards_pile = BinCardsPile([])
    play_service = PlayService()
    card = Card("A", "diamond", "path")
    game = Game(4, True)
    demand = Card("5", "heart", "path")
    cards = [Card("6", "heart", "path"), card]
    player = Player(cards, "player")
    game.current_player = player
    play_service.play_card(card, demand, game, card_on_field, bin_cards_pile)
    assert play_service.ace_demand.color == demand.color
    assert play_service.card_was_played is True


def test_play_card_7_eart():
    card_on_table = Card("7", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    bin_cards_pile = BinCardsPile([])
    play_service = PlayService()
    card = Card("7", "diamond", "path")
    game = Game(4, False)
    demand = None
    cards = [Card("6", "heart", "path"), card]
    player = Player(cards, "player")
    game.current_player = player
    play_service.play_card(card, demand, game, card_on_field, bin_cards_pile)
    assert play_service.jack_demand is None
    assert play_service.jack_counter == 0
    assert play_service.ace_demand is None
    assert play_service.attack_value == 0
    assert play_service.four_counter == 0
    assert play_service.changed_order is False
    assert play_service.active_king_played is False
    assert play_service.protective_card is None
    assert play_service.card_was_played is True


def test_other_action_makao():
    play_service = PlayService()
    command = Command("makao",)
    game = Game(4, True)
    cards_pile = CardsPile()
    bin_cards_pile = BinCardsPile()
    cards = [Card("6", "heart", "path")]
    player = Player(cards, "player")
    game.current_player = player
    play_service.play_other_action(command, game, cards_pile, bin_cards_pile)
    assert game.current_player.said_makao is False


def test_other_action_stop_makao():
    play_service = PlayService()
    command = Command("stop makao")
    game = Game(4, False)
    cards = create_cards()
    cards_pile = CardsPile(cards)
    bin_cards_pile = BinCardsPile()
    cards = [Card("6", "heart", "path")]
    player = Player(cards, "player")
    game.current_player = player
    play_service.play_other_action(command, game, cards_pile, bin_cards_pile)
    assert game.current_player.number_of_cards == 1


def test_other_action_end_turn():
    play_service = PlayService()
    command = Command("end turn")
    cards = create_cards()
    cards_pile = CardsPile(cards)
    game = Game(4, True)
    bin_cards_pile = BinCardsPile()
    play_service.play_other_action(command, game, cards_pile, bin_cards_pile)
    assert game.end_turn is False


def test_is_typical_situation_normal():
    play_service = PlayService()
    assert play_service.is_typical_situation()


def test_is_typical_situation_attack():
    play_service = PlayService()
    play_service.attack_value = 1
    assert not play_service.is_typical_situation()


def test_is_typical_situation_four_counter():
    play_service = PlayService()
    play_service.four_counter = 1
    assert not play_service.is_typical_situation()


def test_is_typical_situation_jack_demand():
    play_service = PlayService()
    play_service.jack_demand = True
    assert not play_service.is_typical_situation()


def test_is_typical_situation_ace_demand():
    play_service = PlayService()
    play_service.ace_demand = True
    assert not play_service.is_typical_situation()


def test_first_saves():
    play_service = PlayService()
    cards = [Card("7", "spade", "path"), Card("A", "diamond", "path")]
    game = Game(4, True)
    cards_pile = CardsPile(cards)
    bin_cards_pile = BinCardsPile()
    cards = [Card("6", "heart", "path")]
    player = Player(cards, "player")
    game.current_player = player
    play_service.first_saves(cards_pile, bin_cards_pile, game)
    assert play_service.protective_card.number == "7"
    assert play_service.protective_card.color == "spade"
    assert play_service.protective_card.image == "path"
    assert len(cards_pile.cards) == 1


def test_take_attack():
    play_service = PlayService()
    play_service.attack_value = 4
    cards = [Card("7", "spade", "path"), Card("A", "diamond", "path"), Card("K", "spade", "path")]
    game = Game(4, False)
    cards_pile = CardsPile(cards)
    bin_cards_pile = BinCardsPile()
    cards = [Card("6", "heart", "path")]
    player = Player(cards, "player")
    game.current_player = player
    play_service.take_attack(cards_pile, bin_cards_pile, game)
    assert play_service.attack_value == 0
    assert len(cards_pile.cards) == 0


def test_take_stop():
    play_service = PlayService()
    play_service.four_counter = 3
    game = Game(4, False)
    cards = [Card("6", "heart", "path")]
    player = Player(cards, "player")
    game.current_player = player
    play_service.take_stop(game)
    assert game.current_player.stop_turns == 3
    assert play_service.four_counter == 0
