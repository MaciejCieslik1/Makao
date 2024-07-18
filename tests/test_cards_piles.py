from cards_piles import Pile, CardsPile, BinCardsPile, CardOnField
from cards import create_cards, Card
from game import Game


def test_pile_create():
    cards = create_cards()
    cards_pile = Pile(cards)
    assert len(cards_pile.cards) == 52


def test_pile_create_empty():
    bin_cards_pile = Pile()
    assert bin_cards_pile.cards == []


def test_bin_cards_pile_create():
    cards = [Card(str(number), "spade", "path") for number in range(2, 11)]
    bin_cards_pile = BinCardsPile(cards)
    assert len(bin_cards_pile.cards) == 9
    assert isinstance(bin_cards_pile.cards, list) is True
    for counter, card in enumerate(bin_cards_pile.cards):
        assert card.number == str(counter + 2)
        assert card.color == "spade"
        assert card.image == "path"


def test_add_card_to_bin():
    card = Card("Q", "club", "path")
    cards = [Card(str(number), "spade", "path") for number in range(2, 11)]
    bin_cards_pile = BinCardsPile(cards)
    bin_cards_pile.add_card_to_bin(card)
    assert len(bin_cards_pile.cards) == 10
    added_card = bin_cards_pile.cards[-1]
    assert added_card.number == "Q"
    assert added_card.color == "club"
    assert added_card.image == "path"


def test_deal_cards_not_enough_cards():
    cards_bin = [Card(str(number), "spade", "path") for number in range(2, 11)]
    bin_cards_pile = BinCardsPile(cards_bin)
    cards = [Card(str(number), "heart", "path") for number in range(2, 4)]
    cards_pile = CardsPile(cards)
    game = Game(4, True)
    assert cards_pile.deal_cards(12, bin_cards_pile, game) is None


def test_deal_cards_enough_cards_in_pile():
    cards_bin = [Card(str(number), "spade", "path") for number in range(2, 4)]
    bin_cards_pile = BinCardsPile(cards_bin)
    cards = [Card(str(number), "heart", "path") for number in range(2, 5)]
    cards_pile = CardsPile(cards)
    ex = [Card("2", "heart", "path"), Card("3", "heart", "path")]
    game = Game(4, True)
    exemplary_dealt_cards = ex
    dealt_cards = cards_pile.deal_cards(2, bin_cards_pile, game)
    assert len(dealt_cards) == 2
    assert len(cards_pile.cards) == 1
    assert cards_pile.cards[0].number == "4"
    assert cards_pile.cards[0].color == "heart"
    assert cards_pile.cards[0].image == "path"
    number = 2
    for counter in range(number):
        ex = exemplary_dealt_cards[counter]
        assert dealt_cards[counter].number == ex.number
        assert dealt_cards[counter].color == ex.color
        assert dealt_cards[counter].image == ex.image


def test_deal_cards_enough_cards_in_bin_pile():
    cards_bin = [Card(str(number), "spade", "path") for number in range(2, 10)]
    bin_cards_pile = BinCardsPile(cards_bin)
    cards = [Card(str(number), "heart", "path") for number in range(2, 4)]
    cards_pile = CardsPile(cards)
    game = Game(4, False)
    dealt_cards = cards_pile.deal_cards(7, bin_cards_pile, game)
    assert len(dealt_cards) == 7
    assert len(cards_pile.cards) == 3
    assert len(bin_cards_pile.cards) == 0


def test_card_on_field_choose_first_card():
    bin_cards_pile = BinCardsPile()
    cards = [Card("Q", "club", "path"), Card("A", "club", "path")]
    cards.extend([Card(str(num), "heart", "path") for num in range(2, 7)])
    cards_pile = CardsPile(cards)
    card_on_field = CardOnField()
    game = Game(4, False)
    card_on_field.choose_first_card(cards_pile, bin_cards_pile, game)
    assert card_on_field.card.number == "5"
    assert card_on_field.card.color == "heart"
    assert card_on_field.card.image == "path"
    assert len(cards_pile.cards) == 1
    for number, card in enumerate(bin_cards_pile.cards):
        print(f"{number + 1}: {card.number} {card.color} {card.image}")
    assert len(bin_cards_pile.cards) == 5


def test_card_on_field_put_card_on_field():
    bin_cards_pile = BinCardsPile()
    card = Card("10", "diamond", "path")
    card_on_field = CardOnField(card)
    new_card = Card("K", "heart", "path")
    card_on_field.put_card_on_field(new_card, bin_cards_pile)
    assert card_on_field.card.number == "K"
    assert card_on_field.card.color == "heart"
    assert card_on_field.card.image == "path"
    assert bin_cards_pile.cards[0].number == "10"
    assert bin_cards_pile.cards[0].color == "diamond"
    assert bin_cards_pile.cards[0].image == "path"
