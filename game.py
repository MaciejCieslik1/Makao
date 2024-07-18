from players import Player, Opponent
from cards import create_cards
from commands import Command, CommandName
from play_service import PlayService
from cards_piles import CardOnField, CardsPile, BinCardsPile
from screens import game_loop_screen, out_of_cards_screen, results_screen
import time
import pygame


WIDTH, HEIGHT = 1800, 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


class Game:
    """Main class, which controls other classes and has some steering parameters."""

    def __init__(self, number_of_players, difficulty):
        """Initializer.

        Arguments:
        number_of_players -- number of participants who have cards
        difficulty -- difficulty level(true if difficulty is hard and false if easy)

        Attributes:
        list_of_players -- list of paticipants(player or opponent class objects) who have cards.
        number_of_players -- number of participants who have cards
        players_who_finished -- list of participants who have no cards left
        current_player -- participant, who is currently on the move
        next_player -- next participant in the list of players, after this who is currently on the move
        end_turn -- parameter, which shows if participant has ended his turn
        human_in_game -- parameter, which shows if player(player class object) still has cards
        out_of_cards -- parameter, which shows if the cards have run out
        difficult -- difficulty level(true if difficulty is hard or false if easy)
        player_class_object -- object of player class, used by check_instance methods
        opponent_class_object -- object of opponnent class, used by check_instance methods
        command_class_object -- object of command class, used by check_instance methods
        """
        self._list_of_players = []
        self._number_of_players = number_of_players
        self._players_who_finished = []
        self._current_player = None
        self._next_player = None
        self._end_turn = False
        self._human_in_game = True
        self._out_of_cards = False
        self._difficult = difficulty
        self._player_class_object = Player([], "example")
        self._opponent_class_object = Opponent([], "example")
        self._command_class_object = Command(None)

    @property
    def list_of_players(self):
        return self._list_of_players

    @list_of_players.setter
    def list_of_players(self, new_list_of_players):
        self._list_of_players = new_list_of_players

    @property
    def number_of_players(self):
        return self._number_of_players

    @number_of_players.setter
    def number_of_players(self, new_number_of_players):
        self._number_of_players = new_number_of_players

    @property
    def players_who_finished(self):
        return self._players_who_finished

    @players_who_finished.setter
    def players_who_finished(self, new_players_who_finished):
        self._players_who_finished = new_players_who_finished

    @property
    def current_player(self):
        return self._current_player

    @current_player.setter
    def current_player(self, new_current_player):
        self._current_player = new_current_player

    @property
    def next_player(self):
        return self._next_player

    @next_player.setter
    def next_player(self, new_next_player):
        self._next_player = new_next_player

    @property
    def end_turn(self):
        return self._end_turn

    @end_turn.setter
    def end_turn(self, new_end_turn):
        self._end_turn = new_end_turn

    @property
    def human_in_game(self):
        return self._human_in_game

    @human_in_game.setter
    def human_in_game(self, new_human_in_game):
        self._human_in_game = new_human_in_game

    @property
    def out_of_cards(self):
        return self._out_of_cards

    @out_of_cards.setter
    def out_of_cards(self, new_out_of_cards):
        self._out_of_cards = new_out_of_cards

    @property
    def difficult(self):
        return self._difficult

    @difficult.setter
    def difficult(self, new_difficult):
        self._out_of_cards = new_difficult

    @property
    def player_class_object(self):
        return self._player_class_object

    @player_class_object.setter
    def player_class_object(self, new_player_class_object):
        self._player_class_object = new_player_class_object

    @property
    def opponent_class_object(self):
        return self._opponent_class_object

    @opponent_class_object.setter
    def opponent_class_object(self, new_opponent_class_object):
        self._opponent_class_object = new_opponent_class_object

    @property
    def command_class_object(self):
        return self._command_class_object

    @command_class_object.setter
    def commmand_class_object(self, new_command_class_object):
        self._command_class_object = new_command_class_object

    def create_players_list(self, number_of_players, cards_pile, bin_cards_pile):
        """Create participants, give them cards and them put them into the list.

        Arguments:
        number_of_players -- number of participants who have cards
        cards_pile -- pile of cards from which participants can take cards
        bin_cards_pile -- second pile of cards, which keeps used cards
        """
        deafult_number_of_cards = 5
        active_player_number = 1
        cards = cards_pile.deal_cards(deafult_number_of_cards, bin_cards_pile, self)
        player = Player(cards, "player")
        list_of_players = [player]
        for number in range(number_of_players - active_player_number):
            cards = cards_pile.deal_cards(deafult_number_of_cards, bin_cards_pile, self)
            name = "opponent" + str(number + active_player_number)
            list_of_players.append(Opponent(cards, name))
        self.list_of_players = list_of_players

    def make_playable_list(self, card_on_field, play_service):
        """For every card on hand check if it is playable. If there is protective_card, check only it's card. Make list of playable cards.

        Arguments:
        card_on_field -- card which is currently in the middle of the table
        play_service -- object which determines current game parameters

        Return:
        Created list of playable cards.
        """
        protective_card = play_service.protective_card
        if protective_card:
            return [protective_card] if protective_card.is_playable(card_on_field, play_service) else []
        return ([card for card in self.current_player.cards if card.is_playable(card_on_field, play_service)])

    def make_same_numbers_list(self, card_on_field):
        """Make list of cards, which have the same number as card lying on the table.

        Arguments:
        card_on_field -- card which is currently in the middle of the table

        Return:
        Created list of same number cards.
        """
        return ([card for card in self.current_player.cards if card.have_same_number(card_on_field.card)])

    def say_stop_makao(self, cards_pile, bin_cards_pile):
        """Deal 5 cards from cards pile and give list of this cads to the participant.

        Arguments:
        cards_pile -- pile of cards from which players can take cards
        bin_cards_pile -- second pile of cards, which keeps used cards
        """
        card_in_list = cards_pile.deal_cards(5, bin_cards_pile, self)
        self.current_player.take(card_in_list)

    def turn(self, play_service, card_on_field, cards_pile, bin_cards_pile):
        """Control participants's turn and connects all blocks of actions, which are held during the turn.

        Arguments:
        play_service -- object which determines current game parameters
        card_on_field -- card which is currently in the middle of the table
        cards_pile -- pile of cards from which players can take cards
        bin_cards_pile -- second pile of cards, which keeps used cards
        """
        play_service.active_king_played = False
        play_service.changed_order = False
        play_service.protective_card = None
        play_service.card_was_played = False
        self._end_turn = False
        card_on_field = card_on_field
        if play_service.jack_counter:
            play_service.jack_counter -= 1
        if play_service.jack_counter == 0:
            play_service.jack_demand = None
        if self.current_player.stop_turns > 0:
            self.current_player.stop_turns -= 1
            if play_service.attack_value == 0:
                self.block_end_turn(play_service, cards_pile, bin_cards_pile, card_on_field)
        if play_service.ace_counter:
            play_service.ace_counter -= 1
        if play_service.ace_counter == 0:
            play_service.ace_demand = None
        playable_cards_list = self.make_playable_list(card_on_field, play_service)
        if playable_cards_list:
            decision = self.make_decision(play_service, cards_pile, bin_cards_pile, card_on_field)
            if self.command_class_object.check_instance(decision):
                if play_service.four_counter == 0:
                    self.block_protective_card_and_attack_checking(play_service, card_on_field, cards_pile, bin_cards_pile)
                else:
                    play_service.take_stop(self)
                    self.block_end_turn(play_service, cards_pile, bin_cards_pile, card_on_field)
            else:
                self.block_play_card(decision, card_on_field, play_service, cards_pile, bin_cards_pile)
        else:
            if play_service.four_counter == 0:
                self.block_protective_card_and_attack_checking(play_service, card_on_field, cards_pile, bin_cards_pile)
            else:
                play_service.take_stop(self)
                self.block_end_turn(play_service, cards_pile, bin_cards_pile, card_on_field)

    def make_decision(self, play_service, cards_pile, bin_cards_pile, card_on_field):
        """Allow participant to make decision, which action will be processed.

        Arguments:
        play_service -- object which determines current game parameters
        cards_pile -- pile of cards from which players can take cards
        bin_cards_pile -- second pile of cards, which keeps used cards
        card_on_field -- card which is currently in the middle of the table

        Return:
        Tuple of card and demand or command, depending on which one was chosen.
        """
        command = Command(CommandName.STOP_MAKAO)
        card_demand_tuple = None
        if self.player_class_object.check_instance(self.current_player):
            while not card_demand_tuple and not command.has_name(CommandName.END_TURN):
                choosen_object = self.current_player.choose_object(card_on_field, play_service, self)
                if self.command_class_object.check_instance(choosen_object):
                    command = choosen_object
                    if command.has_name(CommandName.MAKAO) or command.has_name(CommandName.STOP_MAKAO):
                        play_service.play_other_action(command, self, cards_pile, bin_cards_pile)
                else:
                    card_demand_tuple = choosen_object
        if self.opponent_class_object.check_instance(self.current_player):
            while not card_demand_tuple and not command.has_name(CommandName.END_TURN):
                decision = self.current_player.decide(play_service, self, card_on_field)
                if self.command_class_object.check_instance(decision):
                    command = decision
                else:
                    card_demand_tuple = decision
                return decision
        if card_demand_tuple:
            return card_demand_tuple
        return command

    def block_take_attack(self, play_service, cards_pile, bin_cards_pile):
        """Take attack if there is attack_value parameter.

        Arguments:
        play_service -- object which determines current game parameters
        cards_pile -- pile of cards from which players can take cards
        bin_cards_pile -- second pile of cards, which keeps used cards
        """
        if play_service.attack_value:
            play_service.take_attack(cards_pile, bin_cards_pile, self)

    def block_end_turn(self, play_service, cards_pile, bin_cards_pile, card_on_field):
        """Loop until participant chooses end turn command. Manage actions connected to makao command during the loop.

        Arguments:
        play_service -- object which determines current game parameters
        cards_pile -- pile of cards from which players can take cards
        bin_cards_pile -- second pile of cards, which keeps used cards
        card_on_field -- card which is currently in the middle of the table
        """
        if self.player_class_object.check_instance(self.current_player):
            run = True
            while run:
                choosen_object = game_loop_screen(self.list_of_players, card_on_field, play_service)
                if self.command_class_object.check_instance(choosen_object):
                    if choosen_object.has_name(CommandName.END_TURN):
                        run = False
                    elif choosen_object.has_name(CommandName.MAKAO) and self.current_player.stop_turns == 0:
                        play_service.play_other_action(choosen_object, self, cards_pile, bin_cards_pile)
        if self.current_player.has_makao and not self.current_player.said_makao:
            self.say_stop_makao(cards_pile, bin_cards_pile)
        self.end_turn = True

    def block_play_card(self, decision, card_on_field, play_service, cards_pile, bin_cards_pile):
        """Loop until block_end_of_turn will be proceeded. Allow participant to play cards.
        During loop manage also other commands as makao or stop makao.

        Arguments:
        decision -- participant's decision(tuple of card and demand)
        card_on_field -- card which is currently in the middle of the table
        play_service -- object which determines current game parameters
        cards_pile -- pile of cards from which players can take cards
        bin_cards_pile -- second pile of cards, which keeps used cards
        """
        while not self.end_turn:
            card, demand = decision
            brake_seconds = 1
            if self.opponent_class_object.check_instance(self.current_player):
                time.sleep(brake_seconds)
            if self.current_player.has_makao and not self.current_player.said_makao:
                self.say_stop_makao(cards_pile, bin_cards_pile)
            play_service.play_card(card, demand, self, card_on_field, bin_cards_pile)
            if self.opponent_class_object.check_instance(self.current_player) and self.current_player.has_makao:
                self.current_player.say_makao()
            if self.current_player.number_of_cards == 0:
                time.sleep(brake_seconds)
                self.end_turn = True
            else:
                if play_service.active_king_played is True:
                    self.block_end_turn(play_service, cards_pile, bin_cards_pile, card_on_field)
                else:
                    same_number_list = self.make_same_numbers_list(card_on_field)
                    if same_number_list:
                        decision = self.make_decision(play_service, cards_pile, bin_cards_pile, card_on_field)
                        if self.command_class_object.check_instance(decision):
                            play_service.play_other_action(decision, self, cards_pile, bin_cards_pile)
                    else:
                        self.block_end_turn(play_service, cards_pile, bin_cards_pile, card_on_field)

    def block_protective_card_and_attack_checking(self, play_service, card_on_field, cards_pile, bin_cards_pile):
        """Call first_saves method on play_service object and then take chosen action.
        Chosen action depends on the values of game parameters.

        Arguments:
        card_on_field -- card which is currently in the middle of the table
        play_service -- object which determines current game parameters
        cards_pile -- pile of cards from which players can take cards
        bin_cards_pile -- second pile of cards, which keeps used cards
        """
        play_service.first_saves(cards_pile, bin_cards_pile, self)
        playable_cards_list = self.make_playable_list(card_on_field, play_service)
        if play_service.attack_value == 0:
            if playable_cards_list:
                decision = self.make_decision(play_service, cards_pile, bin_cards_pile, card_on_field)
                if self.command_class_object.check_instance(decision):
                    play_service.play_other_action(decision, self, cards_pile, bin_cards_pile)
                else:
                    self.block_play_card(decision, card_on_field, play_service, cards_pile, bin_cards_pile)
            else:
                self.block_end_turn(play_service, cards_pile, bin_cards_pile, card_on_field)
        else:
            if playable_cards_list:
                decision = self.make_decision(play_service, cards_pile, bin_cards_pile, card_on_field)
                if self.command_class_object.check_instance(decision):
                    self.block_take_attack(play_service, cards_pile, bin_cards_pile)
                else:
                    self.block_play_card(decision, card_on_field, play_service, cards_pile, bin_cards_pile)
            else:
                self.block_take_attack(play_service, cards_pile, bin_cards_pile)

    def game_loop(self):
        """
        Main game loop, which controls all blocks of actions during the game.
        Loop as long as all conditions(1. player has got cards, 2. cards have not run out, 3. number of player is bigger than 1) are met.
        """
        cards = create_cards()
        cards_pile = CardsPile(cards)
        cards_pile.shuffle_cards_pile()
        bin_cards_pile = BinCardsPile()
        play_service = PlayService()
        card_on_field = CardOnField()
        card_on_field.choose_first_card(cards_pile, bin_cards_pile, self)
        counter = 0
        self.out_of_cards = False
        play_service.card_was_played = False
        self.create_players_list(self.number_of_players, cards_pile, bin_cards_pile)
        while self.human_in_game and not self.out_of_cards and self.number_of_players > 1:
            if play_service.changed_order is True:
                go_to_previus_player = 2
                counter -= go_to_previus_player
            self.current_player = self.list_of_players[counter % self.number_of_players]
            self.next_player = self.list_of_players[(counter + 1) % self.number_of_players]
            self._active_king_played = False
            play_service.changed_order = False
            self._protective_card = None
            self._card_was_played = False
            counter += 1
            self.turn(play_service, card_on_field, cards_pile, bin_cards_pile)
            if self.current_player.number_of_cards == 0:
                self.players_who_finished.append(self.current_player)
                if self.player_class_object.check_instance(self.current_player):
                    self.human_in_game = False
                self.list_of_players.remove(self.current_player)
                self.number_of_players -= 1
                counter -= 1
        if self.out_of_cards is True:
            out_of_cards_screen()
        else:
            sorted_players_left = sorted(self.list_of_players, key=lambda player: player.number_of_cards)
            self.players_who_finished.extend(sorted_players_left)
            results_screen(self.players_who_finished)
