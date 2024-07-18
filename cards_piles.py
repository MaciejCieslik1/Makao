from random import shuffle


class Pile:
    """Pile of cards."""

    def __init__(self, cards=None):
        """Initializer

        Optional arguments:
        cards -- list of card objects. Default None.

        Attributes:
        cards -- cards on pile
        """
        self._cards = cards if cards else []

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, new_cards):
        self._cards = new_cards


class CardsPile(Pile):
    """Pile of cards from which players can take cards. Inherit from Pile class."""

    def __init__(self, cards=None):
        """Initializer. Call superior class initializer.

        Optional arguments:
        cards -- list of card objects. Default None.
        """
        super().__init__(cards)

    def shuffle_cards_pile(self):
        """Shuffle cards in random order"""
        shuffle(self.cards)

    def deal_cards(self, number_of_cards, bin_cards_pile, game):
        """Give cards to players, remove these cards from pile and control state of cards pile.

        Arguments:
        number_of_cards -- number of cards which should be given to player and removed from cards pile
        bin_cards_pile -- bin_cards_pile class object
        game -- game class object

        Return:
        List of cards, which should be given to the player.
        """
        if len(self.cards) + len(bin_cards_pile.cards) < number_of_cards:
            cards_to_deal = None
            game.end_turn = True
            game.out_of_cards = True
        elif number_of_cards <= len(self.cards):
            cards_to_deal = self.cards[:number_of_cards]
            self.cards = self.cards[number_of_cards:]
        else:
            cards_to_deal = self.cards
            cards_to_deal_left = number_of_cards - len(cards_to_deal)
            self.cards = bin_cards_pile.cards
            bin_cards_pile.cards = []
            self.shuffle_cards_pile()
            cards_to_deal.extend(self.cards[:cards_to_deal_left])
            self.cards = self.cards[cards_to_deal_left:]
        return cards_to_deal


class BinCardsPile(Pile):
    """Second pile of cards, which keeps used cards."""

    def __init__(self, cards=None):
        """Initializer. Call superior class initializer.

        Optional arguments:
        cards -- list of card objects. Default None.
        """
        super().__init__(cards)

    def add_card_to_bin(self, card):
        """Add card to second(bin) cards pile"""
        self.cards.append(card)


class CardOnField:
    """Card which is currently in the middle of the table."""
    def __init__(self, card=None):
        """Initializer

        Optional arguments:
        card -- card class object which describes which card is on the table. Default None.

        Attributes:
        card -- cards on pile
        """
        self._card = card

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, new_card):
        self._card = new_card

    def choose_first_card(self, cards_pile, bin_cards_pile, game):
        """Choose normal card, which has no special utilities."""
        dealt_card_in_list = cards_pile.deal_cards(1, bin_cards_pile, game)
        special_numbers = ["2", "3", "4", "J", "Q", "K", "A"]
        while dealt_card_in_list[0].number in special_numbers:
            bin_cards_pile.add_card_to_bin(dealt_card_in_list[0])
            dealt_card_in_list = cards_pile.deal_cards(1, bin_cards_pile, game)
        self.card = dealt_card_in_list[0]

    def put_card_on_field(self, card, bin_cards_pile):
        """Set card as a card on the table and put old one onto bin cards pile."""
        bin_cards_pile.add_card_to_bin(self.card)
        self.card = card
