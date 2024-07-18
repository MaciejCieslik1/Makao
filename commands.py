from enum import Enum


class CommandName(Enum):
    """Create variables, which take command names to use them later with enum technique."""
    MAKAO = "makao"
    STOP_MAKAO = "stop makao"
    END_TURN = "end turn"


class Command:
    """Commands, which are controlling the game(makao, stop makao, end turn)."""

    def __init__(self, name):
        """Initializer.

        Arguments:
        name -- name of the command

        Attributes:
        name -- name of the command
        """
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def color(self, new_name):
        self._name = new_name

    def check_instance(self, object):
        """Check if object is an object of the same class as self.

        Return:
        True if clases are the same, false if different.
        """
        return isinstance(object, self.__class__)

    def has_name(self, name):
        """Check if command has name equal to given one.

        Arguments:
        name -- name compared to card name

        Return:
        True or false.
        """
        return (self.name == name)

    def is_enable(self, play_service, game):
        """Check if command can be used, based on current game parameters.

        Arguments:
        play_service -- object which determines current game parameters
        game -- game class object

        Return:
        True if command meets the requirements of being played or false if does not.
        """
        if self.has_name(CommandName.MAKAO):
            return (game.current_player.has_makao)
        elif self.has_name(CommandName.STOP_MAKAO):
            return (game.current_player.has_makao and not game.current_player.said_makao)
        return (bool(play_service.four_counter) or play_service.card_was_played or (bool(play_service.protective_card) and not bool(play_service.attack_value)))
