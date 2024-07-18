from cards import Card
from commands import Command, CommandName
from screens import game_loop_screen, jack_demand_screen, ace_demand_screen, DemandName
from abc import ABC, abstractmethod


class Participant(ABC):
    """Class of game participant."""

    def __init__(self, cards, name):
        """Initializer.

        Arguments:
        cards -- list of participant's cards
        name -- name of participant

        Attributes:
        cards -- list of participant's cards
        number_of_cards -- number of participant's cards
        stop_turns -- number of turn during which participant will be unable to play, except for situation when participant have to defend himself
        has_makao -- parameter which is equal to true when participant has one card on hand and false in other cases
        said_makao -- parameter which is equal to true when participant said makao and false in other cases
        name -- name of participant
        """
        self._cards = cards
        self._number_of_cards = len(self.cards)
        self._stop_turns = 0
        self._has_makao = False
        self._said_makao = False
        self._name = name

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, new_cards):
        self._cards = new_cards

    @property
    def number_of_cards(self):
        return self._number_of_cards

    @number_of_cards.setter
    def number_of_cards(self, new_number_of_cards):
        self._number_of_cards = new_number_of_cards

    @property
    def stop_turns(self):
        return self._stop_turns

    @stop_turns.setter
    def stop_turns(self, new_stop_turns):
        self._stop_turns = new_stop_turns

    @property
    def has_makao(self):
        return self._has_makao

    @has_makao.setter
    def has_makao(self, new_has_makao):
        self._has_makao = new_has_makao

    @property
    def said_makao(self):
        return self._said_makao

    @said_makao.setter
    def said_makao(self, new_said_makao):
        self._said_makao = new_said_makao

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @abstractmethod
    def check_instance(self, object):
        """Create abstact method."""
        pass

    def play(self, card):
        """Remove card from players hand and decrease number of cards by 1. Set has_makao to true when participant has 1 card.

        Arguments:
        card -- card, which will be removed from hand

        Return:
        Removed card.
        """
        self.cards.remove(card)
        self.number_of_cards -= 1
        if self.number_of_cards == 1:
            self.has_makao = True
        return card

    def take(self, list_of_cards):
        """Extend participant's card on hand by extra cards.
        Set has_makao and said_makao attributes to false if number_of_cards is not equal to 1.

        Arguments:
        list_of_cards -- list of cards, which will be added to participant's cards on hand
        """
        if list_of_cards:
            self.cards.extend(list_of_cards)
            self.number_of_cards += len(list_of_cards)
        if self.number_of_cards != 1:
            self.has_makao = False
            self.said_makao = False

    def say_makao(self):
        """Set said_makao attribute to true."""
        self._said_makao = True


class Player(Participant):
    """Class of opponent. Inherit from Participant class."""

    def __init__(self, cards, name):
        """Initializer.

        Arguments:
        cards -- list of participant's cards
        name -- name of participant
        """
        super().__init__(cards, name)

    def check_instance(self, object):
        """Check if object is an object of the same class as self.

        Return:
        True if clases are the same, false if different.
        """
        return isinstance(object, self.__class__)

    def choose_object(self, card_on_field, play_service, game):
        """Choose object, which is card and demand connected to special cards or comand.
        When extra demand is needed, provide that option by displaying demand screens.

        Return:
        Tuple of card and demand when card was selected or command when command was selected.
        """
        run = True
        command_class_object = Command(None)
        while run:
            choosen_object = game_loop_screen(game.list_of_players, card_on_field, play_service)
            if command_class_object.check_instance(choosen_object):
                if choosen_object.is_enable(play_service, game):
                    run = False
            else:
                demand = None
                if choosen_object in game.make_playable_list(card_on_field, play_service):
                    run = False
                    if choosen_object.has_number("J"):
                        run2 = True
                        while run2:
                            demand = jack_demand_screen()
                            if demand:
                                run2 = False
                    elif choosen_object.has_number("A"):
                        run3 = True
                        while run3:
                            demand = ace_demand_screen()
                            if demand:
                                run3 = False
                    if demand == DemandName.DEMAND_NOTHING.value:
                        demand = None
        if command_class_object.check_instance(choosen_object):
            return choosen_object
        return (choosen_object, demand)


class Opponent(Participant):
    """Class of opponent. Inherit from Participant class."""

    def __init__(self, cards, name):
        """Initializer.

        Arguments:
        cards -- list of participant's cards
        name -- name of participant
        """
        super().__init__(cards, name)

    def check_instance(self, object):
        """Check if object is an object of the same class as self.

        Return:
        True if clases are the same, false if different.
        """
        return isinstance(object, self.__class__)

    def choose_card(self, playable_list):
        """Logics connected to opponent, when difficulty level is easy.

        Arguments:
        playable_list -- list of cards, which can be played

        Return:
        Tuple of chosen card and demand.
        """
        card = playable_list[0]
        demand = None
        if card.has_number("J"):
            demand = Card("5", "heart", "path")
        if card.has_number("A"):
            demand = Card("5", "heart", "path")
        return (card, demand)

    def choose_card_hard(self, playable_list, next_player_few_cards):
        """Logics connected to opponent, when difficulty level is hard.

        Arguments:
        playable_list -- list of cards, which can be played
        next_player_few_cards -- parameter, which is false when next participant have more than 2 cards and true in other cases.

        Return:
        Tuple of chosen card and demand.
        """
        if next_player_few_cards:
            cards_dictionary = {"Q": [], "normal_cards": [], "A": [],  "K": [],  "4": [], "J": [],  "2": [], "3": []}
        else:
            cards_dictionary = {"Q": [], "K": [], "3": [], "2": [], "J": [], "4": [], "A": [], "normal_cards": []}
        color_dictionary = {"heart": 0, "diamond": 0, "spade": 0, "club": 0}
        normal_cards_dictionary = {"5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0}
        for card in playable_list:
            if card.number in ["2", "3", "4", "J", "Q", "K", "A"]:
                cards = cards_dictionary[card.number]
                cards.append(card)
                cards_dictionary[card.number] = cards
            else:
                cards = cards_dictionary["normal_cards"]
                cards.append(card)
                cards_dictionary["normal_cards"] = cards
        card = None
        for key, value in cards_dictionary.items():
            if len(value) != 0:
                card = value[0]
        demand = None
        if card.has_number("J"):
            normal_cards = []
            for card_on_hand in self.cards:
                if card_on_hand.number in ["5", "6", "7", "8", "9", "10"]:
                    normal_cards.append(card_on_hand)
            for card2 in normal_cards:
                if card2 != card:
                    amount = normal_cards_dictionary[card2.number]
                    normal_cards_dictionary[card2.number] = amount + 1
            choosen_number = None
            max_value = 0
            for key, value in normal_cards_dictionary.items():
                if value > max_value:
                    choosen_number = key
                    max_value = value
            if choosen_number:
                demand = Card(choosen_number, "heart", "path")
            else:
                demand = None
        if card.has_number("A"):
            for card2 in self.cards:
                if card2 != card:
                    amount = color_dictionary[card2.color]
                    color_dictionary[card2.color] = amount + 1
            choosen_color = "heart"
            max_value = -1
            for key, value in color_dictionary.items():
                if value > max_value:
                    choosen_color = key
                    max_value = value
            demand = Card("5", choosen_color, "path")
        return (card, demand)

    def decide(self, play_service, game, card_on_field):
        """Choose card if there is at least 1 card in playable_list or choose end turn command in other cases.

        Arguments:
        play_service -- object which determines current game parameters
        game -- game class object
        card_on_field -- card which is currently in the middle of the table

        Return:
        Tuple of chosen card and demand or command if playable_list is empty.
        """
        playable_list = game.make_playable_list(card_on_field, play_service)
        if playable_list:
            if game.difficult:
                if game.next_player.number_of_cards <= 2:
                    next_player_few_cards = True
                else:
                    next_player_few_cards = False
                decision = self.choose_card_hard(playable_list, next_player_few_cards)
            else:
                decision = self.choose_card(playable_list)
        else:
            decision = Command(CommandName.END_TURN)
        return decision
