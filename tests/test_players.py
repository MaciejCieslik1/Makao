from cards import Card
from players import Participant, Player, Opponent
from game import Game
from play_service import PlayService
from cards_piles import CardOnField


def test_player_create():
    cards = [Card("Q", "club", "path"), Card("A", "club", "path")]
    player = Player(cards, "Player")
    assert player.number_of_cards == 2
    assert player.stop_turns == 0
    assert player.has_makao is False
    assert player.said_makao is False
    assert player.number_of_cards == 2


def test_player_play():
    cards = [Card("Q", "club", "path"), Card("A", "club", "path")]
    player = Player(cards, "Player")
    played_card = player.play(cards[0])
    assert player.number_of_cards == 1
    assert played_card.number == "Q"
    assert played_card.color == "club"
    assert played_card.image == "path"


def test_player_take():
    take_cards = [Card(str(number), "spade", "path") for number in range(2, 5)]
    cards = [Card("Q", "club", "path"), Card("A", "club", "path")]
    player = Player(cards, "Player")
    player.take(take_cards)
    assert player.number_of_cards == 5


def test_opponent_create():
    cards = [Card("Q", "club", "path"), Card("A", "club", "path")]
    player = Opponent(cards, "opponent")
    assert player.number_of_cards == 2
    assert player.stop_turns == 0
    assert player.has_makao is False
    assert player.said_makao is False
    assert player.number_of_cards == 2


def test_opponent_play():
    cards = [Card("Q", "club", "path"), Card("A", "club", "path")]
    player = Opponent(cards, "opponent")
    played_card = player.play(cards[0])
    assert player.number_of_cards == 1
    assert played_card.number == "Q"
    assert played_card.color == "club"
    assert played_card.image == "path"


def test_opponent_take():
    take_cards = [Card(str(number), "spade", "path") for number in range(2, 5)]
    cards = [Card("Q", "club", "path"), Card("A", "club", "path")]
    player = Opponent(cards, "opponent")
    player.take(take_cards)
    assert player.number_of_cards == 5


def test_opponent_choose_card():
    playable_list = [Card("9", "club", "path"), Card("2", "spade", "path")]
    opponent = Opponent(playable_list, "opponent1")
    card, demand = opponent.choose_card(playable_list)
    assert card.number == "9"
    assert card.color == "club"
    assert card.image == "path"
    assert demand is None


def test_opponent_choose_card_jack():
    playable_list = [Card("J", "club", "path"), Card("2", "spade", "path")]
    opponent = Opponent(playable_list, "opponent1")
    card, demand = opponent.choose_card(playable_list)
    assert card.number == "J"
    assert card.color == "club"
    assert card.image == "path"
    assert demand.number == "5"


def test_opponent_choose_card_ace():
    playable_list = [Card("A", "club", "path"), Card("2", "spade", "path")]
    opponent = Opponent(playable_list, "opponent1")
    card, demand = opponent.choose_card(playable_list)
    assert card.number == "A"
    assert card.color == "club"
    assert card.image == "path"
    assert demand.color == "heart"


def test_opponent_choose_card_hard():
    playable_list = [Card("A", "club", "path"), Card("2", "spade", "path"), Card("6", "spade", "path")]
    opponent = Opponent(playable_list, "opponent1")
    next_player_few_cards = False
    card, demand = opponent.choose_card_hard(playable_list, next_player_few_cards) 
    assert card.number == "6"
    assert card.color == "spade"
    assert demand is None


def test_opponent_choose_card_hard_2():
    playable_list = [Card("K", "club", "path"), Card("2", "spade", "path")]
    opponent = Opponent(playable_list, "opponent1")
    next_player_few_cards = False
    card, demand = opponent.choose_card_hard(playable_list, next_player_few_cards) 
    assert card.number == "2"
    assert card.color == "spade"
    assert demand is None


def test_opponent_choose_card_hard_few_cards_3():
    playable_list = [Card("A", "club", "path"), Card("2", "spade", "path"), Card("6", "spade", "path")]
    opponent = Opponent(playable_list, "opponent1")
    next_player_few_cards = True
    card, demand = opponent.choose_card_hard(playable_list, next_player_few_cards) 
    assert card.number == "2"
    assert card.color == "spade"
    assert demand is None


def test_opponent_choose_card_hard_few_cards_4():
    playable_list = [Card("A", "club", "path"), Card("2", "spade", "path"),  Card("3", "heart", "path"), Card("6", "spade", "path")]
    opponent = Opponent(playable_list, "opponent1")
    next_player_few_cards = True
    card, demand = opponent.choose_card_hard(playable_list, next_player_few_cards) 
    assert card.number == "3"
    assert card.color == "heart"
    assert demand is None


def test_opponent_choose_card_hard_4():
    playable_list = [Card("4", "club", "path"), Card("Q", "spade", "path"), Card("K", "spade", "path")]
    opponent = Opponent(playable_list, "opponent1")
    next_player_few_cards = False
    card, demand = opponent.choose_card_hard(playable_list, next_player_few_cards) 
    assert card.number == "4"
    assert card.color == "club"
    assert demand is None


def test_opponent_choose_card_hard_jack_5():
    card_jack = Card("J", "club", "path")
    cards = [Card("Q", "club", "path"), card_jack, Card("9", "club", "path"), Card("6", "spade", "path"), Card("9", "heart", "path")]
    playable_list = [Card("Q", "club", "path"), card_jack]
    opponent = Opponent(cards, "opponent1")
    next_player_few_cards = False
    card, demand = opponent.choose_card_hard(playable_list, next_player_few_cards) 
    assert card.number == "J"
    assert card.color == "club"
    assert demand.number == "9"


def test_opponent_choose_card_hard_jack_6():
    card_jack = Card("J", "club", "path")
    cards = [Card("Q", "club", "path"), card_jack, Card("8", "club", "path"), Card("7", "spade", "path"), Card("9", "heart", "path")]
    playable_list = [Card("Q", "club", "path"), card_jack]
    opponent = Opponent(cards, "opponent1")
    next_player_few_cards = False
    card, demand = opponent.choose_card_hard(playable_list, next_player_few_cards) 
    assert card.number == "J"
    assert card.color == "club"
    assert demand.number == "7"


def test_opponent_choose_card_hard_jack_7():
    card_jack = Card("J", "club", "path")
    cards = [Card("Q", "club", "path"), card_jack, Card("K", "club", "path"), Card("4", "spade", "path"), Card("3", "heart", "path")]
    playable_list = [Card("Q", "club", "path"), card_jack]
    opponent = Opponent(cards, "opponent1")
    next_player_few_cards = False
    card, demand = opponent.choose_card_hard(playable_list, next_player_few_cards) 
    assert card.number == "J"
    assert card.color == "club"
    assert demand is None


def test_opponent_choose_card_hard_ace_8():
    card_ace = Card("A", "club", "path")
    cards = [Card("Q", "diamond", "path"), card_ace, Card("K", "diamond", "path"), Card("4", "club", "path"), Card("3", "heart", "path")]
    playable_list = [Card("Q", "club", "path"), card_ace]
    opponent = Opponent(cards, "opponent1")
    next_player_few_cards = False
    card, demand = opponent.choose_card_hard(playable_list, next_player_few_cards) 
    assert card.number == "A"
    assert card.color == "club"
    assert demand.color == "diamond"


def test_opponent_choose_card_hard_ace_9():
    card_ace = Card("A", "club", "path")
    cards = [Card("Q", "diamond", "path"), card_ace, Card("K", "spade", "path"), Card("4", "club", "path"), Card("3", "heart", "path")]
    playable_list = [Card("Q", "club", "path"), card_ace]
    opponent = Opponent(cards, "opponent1")
    next_player_few_cards = False
    card, demand = opponent.choose_card_hard(playable_list, next_player_few_cards) 
    assert card.number == "A"
    assert card.color == "club"
    assert demand.color == "heart"



def test_opponent_decide():
    game = Game(4, False)
    play_service = PlayService()
    card_on_field = CardOnField(Card("6", "diamond", "path"))
    cards = [Card("6", "club", "path"), Card("J", "diamond", "path"), Card("5", "heart", "path")]
    opponent = Opponent(cards, "opponent1")
    game.current_player = opponent
    decision = game.current_player.decide(play_service, game, card_on_field)
    card, demand = decision
    assert card.number == "6"
    assert card.color == "club"
    assert card.image == "path"
    assert demand is None


def test_opponent_decide_demand():
    game = Game(4, False)
    play_service = PlayService()
    card_on_field = CardOnField(Card("7", "diamond", "path"))
    cards = [Card("6", "club", "path"), Card("J", "diamond", "path"), Card("5", "heart", "path")]
    opponent = Opponent(cards, "opponent1")
    game.current_player = opponent
    decision = game.current_player.decide(play_service, game, card_on_field)
    card, demand = decision
    assert card.number == "J"
    assert card.color == "diamond"
    assert card.image == "path"
    assert demand.number == "5"


def test_opponent_decide_protective_card():
    game = Game(4, False)
    play_service = PlayService()
    card_on_field = CardOnField(Card("7", "spade", "path"))
    cards = [Card("6", "club", "path"), Card("J", "diamond", "path"), Card("5", "heart", "path")]
    opponent = Opponent(cards, "opponent1")
    game.current_player = opponent
    play_service.protective_card = Card("4", "spade", "path")
    decision = game.current_player.decide(play_service, game, card_on_field)
    card, demand = decision
    assert card.number == "4"
    assert card.color == "spade"
    assert card.image == "path"
    assert demand is None
