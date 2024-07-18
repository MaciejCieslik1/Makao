from commands import CommandName


class PlayService:
    """Class, which keeps important game parameters."""

    def __init__(self):
        """Initializer.

        Attributes:
        jack_demand -- demand descibed as card object with chosen number
        jack_counter -- number of turns, after which demand will not be active
        ace_demand -- demand descibed as card object with chosen color
        ace_counter -- number of turns, after which demand will not be active
        attack_value -- number of cards, which will be dealt to participant, who cannot defend himself
        four_counter --  number of stop turns, which will be given to player who cannot defend himself
        active_king_played -- parameter, which shows if the active king was played in current turn
        protecive card -- card, which was taken by participant, from card pile, as a defensive card
        card_was_played -- parameter, which shows if card was any card was played in current turn
        card_on_field -- card which is currently in the middle of the table
        """
        self._jack_demand = None
        self._jack_counter = 0
        self._ace_demand = None
        self._ace_counter = 0
        self._attack_value = 0
        self._four_counter = 0
        self._active_king_played = False
        self._changed_order = False
        self._protective_card = None
        self._card_was_played = False
        self._card_on_field = None

    @property
    def jack_demand(self):
        return self._jack_demand

    @jack_demand.setter
    def jack_demand(self, new_jack_demand):
        self._jack_demand = new_jack_demand

    @property
    def jack_counter(self):
        return self._jack_counter

    @jack_counter.setter
    def jack_counter(self, new_jack_counter):
        self._jack_counter = new_jack_counter

    @property
    def ace_demand(self):
        return self._ace_demand

    @ace_demand.setter
    def ace_demand(self, new_ace_demand):
        self._ace_demand = new_ace_demand

    @property
    def ace_counter(self):
        return self._ace_counter

    @ace_counter.setter
    def ace_counter(self, new_ace_counter):
        self._ace_counter = new_ace_counter

    @property
    def attack_value(self):
        return self._attack_value

    @attack_value.setter
    def attack_value(self, new_attack_value):
        self._attack_value = new_attack_value

    @property
    def four_counter(self):
        return self._four_counter

    @four_counter.setter
    def four_counter(self, new_four_counter):
        self._four_counter = new_four_counter

    @property
    def active_king_played(self):
        return self._active_king_played

    @active_king_played.setter
    def active_king_played(self, new_active_king_played):
        self._active_king_played = new_active_king_played

    @property
    def changed_order(self):
        return self._changed_order

    @changed_order.setter
    def changed_order(self, new_changed_order):
        self._changed_order = new_changed_order

    @property
    def protective_card(self):
        return self._protective_card

    @protective_card.setter
    def protective_card(self, new_protective_card):
        self._protective_card = new_protective_card

    @property
    def card_was_played(self):
        return self._card_was_played

    @card_was_played.setter
    def card_was_played(self, new_card_was_played):
        self._card_was_played = new_card_was_played

    @property
    def card_on_field(self):
        return self._card_on_field

    @card_on_field.setter
    def card_on_field(self, new_card_on_field):
        self._card_on_field = new_card_on_field

    def play_card(self, card, demand, game, card_on_field, bin_cards_pile):
        """Change the game parameters, according to the attributes of card.

        Arguments:
        card -- card, which number and color atributes are used to change game parameters
        demand -- demand descibed as card object with chosen number or color
        game -- game class object
        card_on_field -- card which is currently in the middle of the table
        bin_cards_pile -- second pile of cards, which keeps used cards
        """
        king_attack_value = 5
        if card.number in {"2", "3"}:
            self.attack_value += int(card.number)
        if card.has_number("K") and card.has_color("heart"):
            self.attack_value += king_attack_value
            self.active_king_played = True
        if card.has_number("K") and card.has_color("spade"):
            self.attack_value += king_attack_value
            self.active_king_played = True
            self.changed_order = True
        if card.has_number("4"):
            self.four_counter += 1
        if card.has_number("J"):
            if demand:
                self.jack_demand = demand
                if game.current_player.number_of_cards > 1:
                    self.jack_counter = game.number_of_players + 1
                else:
                    self.jack_counter = game.number_of_players
            else:
                self.jack_demand = None
        if card.has_number("K") and card.color in {"diamond", "club"}:
            self.active_king_played = False
            self.attack_value = 0
        if card.has_number("A"):
            if demand:
                next_turn_counter = 2
                self.ace_demand = demand
                self.ace_counter = next_turn_counter
            else:
                self.ace_demand = None
        game.current_player.play(card)
        self.card_was_played = True
        bin_cards_pile.cards.append(card_on_field.card)
        card_on_field.card = card

    def play_other_action(self, command, game, cards_pile, bin_cards_pile):
        """Call different actions, depending on which command was chosen.

        Arguments:
        command - chosen command(makao, stop makao or end turn)
        game -- game class object
        cards_pile -- pile of cards from which players can take cards
        bin_cards_pile -- second pile of cards, which keeps used cards
        """
        if command.has_name(CommandName.MAKAO):
            game.current_player.say_makao()
        if command.has_name(CommandName.STOP_MAKAO):
            not_said_makao_fee = 5
            cards_to_deal = cards_pile.deal_cards(not_said_makao_fee, bin_cards_pile, game)
            game.current_player.take(cards_to_deal)
        if command.has_name(CommandName.END_TURN):
            game.end_turn = True

    def is_typical_situation(self):
        """Check if the situation in the game is typical.

        Return:
        True if condition is met or false if not.
        """
        return (not (bool(self.jack_demand) + bool(self.ace_demand) + bool(self.attack_value) + bool(self.four_counter)))

    def first_saves(self, cards_pile, bin_cards_pile, game):
        """Deal one card from card pile and give it to the participant.

        Arguments:
        cards_pile -- pile of cards from which players can take cards
        bin_cards_pile -- second pile of cards, which keeps used cards
        game -- game class objects
        """
        cards_to_deal_number = 1
        card_in_list = cards_pile.deal_cards(cards_to_deal_number, bin_cards_pile, game)
        game.current_player.take(card_in_list)
        self.protective_card = card_in_list[0]

    def take_attack(self, cards_pile, bin_cards_pile, game):
        """Deal that number of cards from cards pile, which equal to attack_value parameter and give them to player.

        Arguments:
        cards_pile -- pile of cards from which players can take cards
        bin_cards_pile -- second pile of cards, which keeps used cards
        game -- game class objects
        """
        cards = cards_pile.deal_cards(self.attack_value - 1, bin_cards_pile, game)
        game.current_player.take(cards)
        self.attack_value = 0

    def take_stop(self, game):
        """Increase participant's stop_turns attribute by value of four_counter parameters. Set 0 value to four counter."""
        game.current_player.stop_turns += self.four_counter
        self.four_counter = 0
