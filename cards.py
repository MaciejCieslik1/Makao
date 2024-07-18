import csv


class Card:
    """Ordinary playing card."""

    def __init__(self, number, color, image):
        """Initializer.

        Arguments:
        number -- number of card
        color -- color of card
        image -- image of the card

        Attributes:
        number -- number of card
        color -- color of card
        image -- image of the card
        """
        self._number = number
        self._color = color
        self._image = image

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, new_number):
        self._number = new_number

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, new_image):
        self._image = new_image

    def have_same_number(self, card):
        """Check if two cards have the same number.

        Arguments:
        card -- second card which is compared with first one

        Return:
        True or false.
        """
        return (self.number == card.number)

    def have_same_color(self, card):
        """Check if two cards have the same color.

        Arguments:
        card -- second card which is compared with first one

        Return:
        True or false.
        """
        return (self.color == card.color)

    def has_number(self, number):
        """Check if card has number equal to given one.

        Arguments:
        number -- number compared to card number

        Return:
        True or false.
        """
        return (self.number == number)

    def has_color(self, color):
        """Check if card has color equal to given one.

        Arguments:
        color -- color compared to card color

        Return:
        True or false.
        """
        return (self.color == color)

    def is_playable(self, card_on_field, play_service):
        """Check if card can be played on the card, which is lying in the middle of the table.

        Arguments:
        card_on_field -- card lying in the middle of the table
        play_service -- object which determines current game parameters

        Return:
        True if card can be played and false when it is not possible.
        """
        if play_service.is_typical_situation() is True:
            if self.has_number("Q") or card_on_field.card.number == "Q":
                return True
            return (self.have_same_number(card_on_field.card) or self.have_same_color(card_on_field.card))
        else:
            list = ["2", "3"]
            if card_on_field.card.number in list:
                if self.number in list:
                    if self.have_same_number(card_on_field.card):
                        return True
                    return (self.have_same_color(card_on_field.card))
                if self.has_number("K"):
                    if self.has_color("heart") and self.have_same_color(card_on_field.card):
                        return True
                    return (self.has_color("spade") and self.have_same_color(card_on_field.card))
            elif card_on_field.card.number == "K":
                return self.has_number("K")
            if play_service.four_counter:
                return (self.has_number("4"))
            if play_service.jack_demand:
                if self.have_same_number(play_service.jack_demand):
                    return True
                return (self.has_number("J") and ((self.have_same_number(card_on_field.card) or self.have_same_color(card_on_field.card))))
            if play_service.ace_demand:
                if self.have_same_color(play_service.ace_demand):
                    return True
                return (self.has_number("A"))


def create_cards():
    """Create card class objects from data from the file.

    Return:
    List of created cards.
    """
    cards = []
    with open("configuration.txt") as configuration_handle:
        cards_file_path = configuration_handle.readline()
        cards_file_path = cards_file_path.rstrip()
    with open(cards_file_path) as file_handle:
        reader = csv.DictReader(file_handle, ["number", "color", "image"])
        for line in reader:
            number, color, image = line["number"], line["color"], line["image"]
            card = Card(number, color, image)
            cards.append(card)
    return cards
