from cards import create_cards, Card
from play_service import PlayService
from cards_piles import CardOnField


def test_create_cards():
    cards = create_cards()
    assert len(cards) == 52
    assert cards[0].number == "2"
    assert cards[0].color == "heart"
    assert cards[0].image == "images/cards/2H.png"


def test_cards_have_same_number():
    card1 = Card("Q", "spade", "path")
    card2 = Card("Q", "heart", "path")
    assert card1.number == card2.number


def test_cards_have_color_number():
    card1 = Card("Q", "diamond", "path")
    card2 = Card("4", "diamond", "path")
    assert card1.color == card2.color


def test_card_has_number():
    card = Card("Q", "spade", "path")
    assert card.number == "Q"


def test_card_has_color():
    card = Card("Q", "spade", "path")
    assert card.color == "spade"


def test_card_is_playable_same_number():
    play_service = PlayService()
    card = Card("10", "club", "path")
    card_on_table = Card("10", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_same_color():
    play_service = PlayService()
    card = Card("10", "club", "path")
    card_on_table = Card("9", "club", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_queen_on_field():
    play_service = PlayService()
    card = Card("10", "club", "path")
    card_on_table = Card("Q", "diamond", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_queen():
    play_service = PlayService()
    card = Card("10", "club", "path")
    card_on_table = Card("Q", "diamond", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_2():
    play_service = PlayService()
    card = Card("2", "diamond", "path")
    card_on_table = Card("6", "diamond", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_2_on_field_6_same_color_normal():
    play_service = PlayService()
    card = Card("6", "spade", "path")
    card_on_table = Card("2", "spade", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_2_on_field_6_normal():
    play_service = PlayService()
    card = Card("6", "diamond", "path")
    card_on_table = Card("2", "spade", "path")
    card_on_field = CardOnField(card_on_table)
    assert not card.is_playable(card_on_field, play_service)


def test_card_is_playable_4_on_field_6_same_color_normal():
    play_service = PlayService()
    card = Card("6", "spade", "path")
    card_on_table = Card("4", "spade", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_jack_on_field_6_same_color_normal():
    play_service = PlayService()
    card = Card("6", "spade", "path")
    card_on_table = Card("jack", "spade", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_ace_on_field_6_same_color_normal():
    play_service = PlayService()
    card = Card("6", "spade", "path")
    card_on_table = Card("jack", "spade", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_2_on_field_6_same_color_attack():
    play_service = PlayService()
    play_service.attack_value = 2
    card = Card("6", "spade", "path")
    card_on_table = Card("2", "spade", "path")
    card_on_field = CardOnField(card_on_table)
    assert not card.is_playable(card_on_field, play_service)


def test_card_is_playable_2_on_field_3_same_color_attack():
    play_service = PlayService()
    play_service.attack_value = 2
    card = Card("3", "spade", "path")
    card_on_table = Card("2", "spade", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_3_on_field_2_same_color_attack():
    play_service = PlayService()
    play_service.attack_value = 2
    card = Card("2", "spade", "path")
    card_on_table = Card("3", "spade", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_2_on_field_3_attack():
    play_service = PlayService()
    play_service.attack_value = 2
    card = Card("3", "club", "path")
    card_on_table = Card("2", "spade", "path")
    card_on_field = CardOnField(card_on_table)
    assert not card.is_playable(card_on_field, play_service)


def test_card_is_playable_2_on_field_2_attack():
    play_service = PlayService()
    play_service.attack_value = 2
    card = Card("2", "spade", "path")
    card_on_table = Card("2", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_2_on_field_Q_attack():
    play_service = PlayService()
    play_service.attack_value = 2
    card = Card("2", "spade", "path")
    card_on_table = Card("Q", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    assert not card.is_playable(card_on_field, play_service)


def test_card_is_playable_2_heart_on_field_king_heart_attack():
    play_service = PlayService()
    play_service.attack_value = 2
    card = Card("K", "heart", "path")
    card_on_table = Card("2", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_2_spade_on_field_king_spade_attack():
    play_service = PlayService()
    play_service.attack_value = 2
    card = Card("K", "heart", "path")
    card_on_table = Card("2", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_3_heart_on_field_king_heart_attack():
    play_service = PlayService()
    play_service.attack_value = 3
    card = Card("K", "heart", "path")
    card_on_table = Card("3", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_3_spade_on_field_king_spade_attack():
    play_service = PlayService()
    play_service.attack_value = 3
    card = Card("K", "heart", "path")
    card_on_table = Card("3", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_3_spade_on_field_king_heart_attack():
    play_service = PlayService()
    play_service.attack_value = 3
    card = Card("K", "heart", "path")
    card_on_table = Card("3", "spade", "path")
    card_on_field = CardOnField(card_on_table)
    assert not card.is_playable(card_on_field, play_service)


def test_card_is_playable_2_heart_on_field_king_spade_attack():
    play_service = PlayService()
    play_service.attack_value = 2
    card = Card("K", "spade", "path")
    card_on_table = Card("2", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    assert not card.is_playable(card_on_field, play_service)


def test_card_is_playable_2_heart_on_field_king_diamond_attack():
    play_service = PlayService()
    play_service.attack_value = 2
    card = Card("K", "diamond", "path")
    card_on_table = Card("2", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    assert not card.is_playable(card_on_field, play_service)


def test_card_is_playable_3_heart_on_field_king_diamond_attack():
    play_service = PlayService()
    play_service.attack_value = 3
    card = Card("K", "club", "path")
    card_on_table = Card("3", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    assert not card.is_playable(card_on_field, play_service)


def test_card_is_playable_K_heart_on_field_K_spade_attack():
    play_service = PlayService()
    play_service.attack_value = 5
    card = Card("K", "spade", "path")
    card_on_table = Card("K", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_K_spade_on_field_K_heart_attack():
    play_service = PlayService()
    play_service.attack_value = 5
    card = Card("K", "heart", "path")
    card_on_table = Card("K", "spade", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_K_spade_on_field_K_club_attack():
    play_service = PlayService()
    play_service.attack_value = 5
    card = Card("K", "club", "path")
    card_on_table = Card("K", "spade", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_K_heart_on_field_K_diamond_attack():
    play_service = PlayService()
    play_service.attack_value = 5
    card = Card("K", "diamond", "path")
    card_on_table = Card("K", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_K_heart_on_field_2_heart_attack():
    play_service = PlayService()
    play_service.attack_value = 5
    card = Card("2", "heart", "path")
    card_on_table = Card("K", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    assert not card.is_playable(card_on_field, play_service)


def test_card_is_playable_K_spade_on_field_3_spade_attack():
    play_service = PlayService()
    play_service.attack_value = 5
    card = Card("3", "spade", "path")
    card_on_table = Card("K", "spade", "path")
    card_on_field = CardOnField(card_on_table)
    assert not card.is_playable(card_on_field, play_service)


def test_card_is_playable_K_spade_on_field_2_spade_normal():
    play_service = PlayService()
    play_service.attack_value = 0
    card = Card("2", "heart", "path")
    card_on_table = Card("K", "heart", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_4_spade_on_field_7_spade_normal():
    play_service = PlayService()
    card = Card("7", "spade", "path")
    card_on_table = Card("4", "spade", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_4_spade_on_field_Q_stop():
    play_service = PlayService()
    play_service.four_counter = 1
    card = Card("Q", "spade", "path")
    card_on_table = Card("4", "spade", "path")
    card_on_field = CardOnField(card_on_table)
    assert not card.is_playable(card_on_field, play_service)


def test_card_is_playable_4_spade_on_field_2_stop():
    play_service = PlayService()
    play_service.four_counter = 1
    card = Card("2", "spade", "path")
    card_on_table = Card("4", "spade", "path")
    card_on_field = CardOnField(card_on_table)
    assert not card.is_playable(card_on_field, play_service)


def test_card_is_playable_4_spade_on_field_4_stop():
    play_service = PlayService()
    play_service.four_counter = 1
    card = Card("4", "diamond", "path")
    card_on_table = Card("4", "spade", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_J_club_on_field_6_club_normal():
    play_service = PlayService()
    play_service.jack_demand = None
    card = Card("J", "club", "path")
    card_on_table = Card("6", "club", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_J_club_on_field_6_club_demand_7():
    play_service = PlayService()
    jack_card = Card("7", "diamond", "path")
    play_service.jack_demand = jack_card
    card = Card("6", "club", "path")
    card_on_table = Card("J", "club", "path")
    card_on_field = CardOnField(card_on_table)
    assert not card.is_playable(card_on_field, play_service)


def test_card_is_playable_7_club_on_field_6_club_demand_7():
    play_service = PlayService()
    jack_card = Card("7", "diamond", "path")
    play_service.jack_demand = jack_card
    card = Card("6", "club", "path")
    card_on_table = Card("7", "club", "path")
    card_on_field = CardOnField(card_on_table)
    assert not card.is_playable(card_on_field, play_service)


def test_card_is_playable_7_club_on_field_Q_club_demand_7():
    play_service = PlayService()
    jack_card = Card("7", "diamond", "path")
    play_service.jack_demand = jack_card
    card = Card("Q", "club", "path")
    card_on_table = Card("7", "club", "path")
    card_on_field = CardOnField(card_on_table)
    assert not card.is_playable(card_on_field, play_service)


def test_card_is_playable_J_club_on_field_7_club_demand_7():
    play_service = PlayService()
    jack_card = Card("7", "diamond", "path")
    play_service.jack_demand = jack_card
    card = Card("7", "club", "path")
    card_on_table = Card("J", "club", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_J_club_on_field_J_heart_demand_7():
    play_service = PlayService()
    jack_card = Card("7", "diamond", "path")
    play_service.jack_demand = jack_card
    card = Card("J", "heart", "path")
    card_on_table = Card("J", "club", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_7_club_on_field_J_club_demand_7():
    play_service = PlayService()
    jack_card = Card("7", "diamond", "path")
    play_service.jack_demand = jack_card
    card = Card("J", "club", "path")
    card_on_table = Card("7", "club", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_7_club_on_field_J_diamond_demand_7():
    play_service = PlayService()
    jack_card = Card("7", "diamond", "path")
    play_service.jack_demand = jack_card
    card = Card("J", "diamond", "path")
    card_on_table = Card("7", "club", "path")
    card_on_field = CardOnField(card_on_table)
    assert not card.is_playable(card_on_field, play_service)


def test_card_is_playable_A_club_on_field_J_club_normal():
    play_service = PlayService()
    card = Card("J", "club", "path")
    card_on_table = Card("A", "club", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_A_club_on_field_J_heart_demand_heart():
    play_service = PlayService()
    ace_card = Card("7", "heart", "path")
    play_service.ace_demand = ace_card
    card = Card("J", "heart", "path")
    card_on_table = Card("A", "club", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)


def test_card_is_playable_A_club_on_field_J_spade_demand_heart():
    play_service = PlayService()
    ace_card = Card("7", "heart", "path")
    play_service.ace_demand = ace_card
    card = Card("J", "spade", "path")
    card_on_table = Card("A", "club", "path")
    card_on_field = CardOnField(card_on_table)
    assert not card.is_playable(card_on_field, play_service)


def test_card_is_playable_A_club_on_field_A_spade_demand_heart():
    play_service = PlayService()
    ace_card = Card("7", "heart", "path")
    play_service.ace_demand = ace_card
    card = Card("A", "spade", "path")
    card_on_table = Card("A", "club", "path")
    card_on_field = CardOnField(card_on_table)
    assert card.is_playable(card_on_field, play_service)
