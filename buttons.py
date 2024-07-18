import pygame
from commands import Command, CommandName


class CardButton:
    """Button object with image of card."""

    def __init__(self, x, y, image, scale):
        """Initializer.

        Arguments:
        x -- horizontal coordinate of button's top left corner
        y -- vertical coordinate of button's top left corner
        image -- image on the button
        scale -- measurements multiplier

        Atributes:
        width -- button's width
        height -- button's height
        rect -- rectangularly shaped surface of the image
        rect.topleft -- coordinates of rectangular's top left corner
        clicked -- click state with values true or false
        """
        self._width = image.get_width()
        self._height = image.get_height()
        self._image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self._rect = self.image.get_rect()
        self._rect.topleft = (x, y)
        self._clicked = False

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, new_width):
        self._width = new_width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, new_height):
        self._height = new_height

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, new_image):
        self._image = new_image

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, new_rect):
        self._rect = new_rect

    @property
    def clicked(self):
        return self._clicked

    @clicked.setter
    def clicked(self, new_clicked):
        self._clicked = new_clicked

    def draw(self, screen):
        """Draw button on the screen and capture clicks, based on mouse state.

        Arguments:
        screen -- screen displayed by pygame

        Return:
        Action state true when mouse button is clicked or false if not.
        """
        action = False
        pos = pygame.mouse.get_pos()
        mouse_y = pos[1]
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.rect.collidepoint(pos):
            if mouse_y > 740:
                circle_center = (self.rect.x + 69, self.rect.y - 20)
                pygame.draw.circle(screen, (0, 0, 255), circle_center, 10)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                action = True
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        return action


class Button:
    """Button with image generated by pygame."""

    def __init__(self, x, y, width, height, color, text, font_size):
        """Initializer.

        Arguments:
        x -- horizontal coordinate of button's top leftcorner
        y -- vertical coordinate of button's top left corner
        width -- button's width
        height -- button's height
        color -- button's color described as a tuple of three RGB parameters
        text -- text displayed on the button
        font_size -- size of the font used in text

        Atributes:
        rect -- rectangularly shaped surface of the image
        color -- button's color, described as a tuple of three RGB parameters
        backlight_color -- color of the covered button, described as a tuple of three RGB parameters
        text -- text displayed on the button
        font_size -- size of the font used in text
        clicked -- click state with values true or false
        """
        self._rect = pygame.Rect(x, y, width, height)
        self._color = color
        self._backlight_color = (0, 0, 255)
        self._text = text
        self._font_size = font_size
        self._clicked = False

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, new_rect):
        self._rect = new_rect

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color

    @property
    def backlight_color(self):
        return self._backlight_color

    @backlight_color.setter
    def backlight_color(self, new_backlight_color):
        self._backlight_color = new_backlight_color

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, new_text):
        self._text = new_text

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def fonr_size(self, new_font_size):
        self._font_size = new_font_size

    @property
    def clicked(self):
        return self._clicked

    @clicked.setter
    def clicked(self, new_clicked):
        self._clicked = new_clicked

    def draw(self, screen):
        """Draw button on the screen and capture clicks, based on mouse state.

        Arguments:
        screen -- screen displayed by pygame

        Return:
        Action state true when mouse button is clicked or false if not.
        """
        pygame.draw.rect(screen, self.color, self.rect, 0)
        font = pygame.font.Font(None, self.font_size)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            pygame.draw.rect(screen, self.backlight_color, self.rect)
            screen.blit(text, text_rect)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        return action


def draw_control_buttons(screen):
    """Draw makao, stop makao and end turn buttons, and check if any button is clicked.

    Arguments:
    screen -- screen displayed by pygame

    Return:
    Name of the command(makao, stop makao or end turn) when draw function returns true.
    """
    makao_button = Button(625, 650, 150, 50, (245, 132, 66), "MAKAO", 30)
    stop_makao_button = Button(825, 650, 150, 50, (245, 132, 66), "STOP MAKAO", 30)
    end_turn_button = Button(1025, 650, 150, 50, (245, 132, 66), "END TURN", 30)
    if makao_button.draw(screen):
        return Command(CommandName.MAKAO)
    if stop_makao_button.draw(screen):
        return Command(CommandName.STOP_MAKAO)
    if end_turn_button.draw(screen):
        return Command(CommandName.END_TURN)


def draw_player_cards(player, screen):
    """Draw player's cards and player's name, and check if any card button is clicked.

    Arguments:
    screen -- screen displayed by pygame

    Return:
    Card object when draw function returns true.
    """
    cards = player.cards
    scaled_card_width = 138
    table_width = 1700
    choosen_card = None
    if player.number_of_cards * scaled_card_width > table_width:
        uncovered_width = (table_width - scaled_card_width) // (player.number_of_cards - 1)
        beginning_gap = 50
    else:
        uncovered_width = 138
        beginning_gap = 900 - (player.number_of_cards * uncovered_width) // 2
    for number, card in enumerate(cards):
        image = pygame.image.load(card.image).convert_alpha()
        x = beginning_gap + uncovered_width * number
        card_on_hand = CardButton(x, 750, image, 0.2)
        if card_on_hand.draw(screen):
            choosen_card = card
    draw_text("player", 300, 700, 40, screen)
    return choosen_card


def draw_opponent_cards(opponent, screen):
    """Draw opponent's cards and opponent's name, on different coordinates for each opponent.

    Arguments:
    screen -- screen displayed by pygame
    """
    name = opponent.name
    if name == "opponent1":
        x = 100
        y = 431
        image = pygame.image.load("images/red_back_rotated.png").convert_alpha()
        draw_text("opponent1", 205, 400, 40, screen)
        draw_number_of_cards(opponent, 450, 500, screen)
    elif name == "opponent2":
        x = 831
        y = 90
        image = pygame.image.load("images/red_back.png").convert_alpha()
        draw_text("opponent2", 900, 60, 40, screen)
        draw_number_of_cards(opponent, 900, 330, screen)
    else:
        x = 1472
        y = 431
        image = pygame.image.load("images/red_back_rotated.png").convert_alpha()
        draw_text("opponent3", 1580, 400, 40, screen)
        draw_number_of_cards(opponent, 1325, 500, screen)
    card_on_hand = CardButton(x, y, image, 0.2)
    card_on_hand.draw(screen)


def draw_all_opponents(list_of_players, screen):
    """Draw cards and name for every opponent in game.

    Arguments:
    screen -- screen displayed by pygame
    """
    for participant in list_of_players:
        if participant.name != "player":
            draw_opponent_cards(participant, screen)


def draw_text(text, x, y, font, screen):
    """Draw text on given coordinates of screen.

    Arguments:
    text -- text displayed on the button
    x -- horizontal coordinate of button's top leftcorner
    y -- vertical coordinate of button's top left corner
    font_size -- size of the font used in text
    screen -- screen displayed by pygame
    """
    font = pygame.font.Font(None, font)
    text_color = (255, 255, 255)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


def draw_number_of_cards(opponent, x, y, screen):
    """Draw number of opponent's cards.

    Arguments:
    opponent -- opponent class object
    text -- text displayed on the button
    x -- horizontal coordinate of button's top left corner
    y -- vertical coordinate of button's top left corner
    screen -- screen displayed by pygame
    """
    number_of_cards = f"Number of cards: {opponent.number_of_cards}"
    font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)
    name_surface = font.render(number_of_cards, True, text_color)
    name_rect = name_surface.get_rect()
    name_rect.center = (x, y)
    screen.blit(name_surface, name_rect)


def draw_card_on_table(card_on_field, x, y, screen):
    """Draw main card in the centre of the table.

    Arguments:
    card_on_field -- card in the centre of the table
    x -- horizontal coordinate of button's top left corner
    y -- vertical coordinate of button's top left corner
    screen -- screen displayed by pygame
    """
    image = pygame.image.load(card_on_field.card.image).convert_alpha()
    card_on_table = CardButton(x, y, image, 0.2)
    card_on_table.draw(screen)
