from TicTacToeText import Impossible, Player, Random, RandomNotStupid
import pygame

pygame.init()
# constants
# fonts
SMALL_FONT = pygame.font.SysFont('arialblack', 20)
END_FONT = pygame.font.SysFont('arialblack', 40)
#colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREY = (220, 220, 220)
GREY = (169, 169, 169)
GREEN = (0, 166, 44)
DARK_GREEN = (49, 115, 60)
PURPLE = (46, 14, 92)
TEAL = (133, 220, 218)
DARK_TEAL = (35, 183, 179)
#display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
#board edges and lines
BOARD_LINES = [75, 225, 375, 525]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Human(Player):
    """
    A human player. Moves are determined by user input.
    
    Attributes
        - tile_type: :class:`str` – which marker this player puts down
        - name: :class:`str` – the name of this player
    """

    def __init__(self, tile_type, name):
        super().__init__(tile_type, name)

    def move(self, has_first_turn: bool, available: set, other_player_moves: list) -> int:
        """Returns which square the player wants to play their move on."""
        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                #check if a tile is clicked on
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BOARD_LINES[0] <= mouse[0] <= BOARD_LINES[1] and BOARD_LINES[0] <= mouse[1] <= BOARD_LINES[1]:
                        return 0
                    elif BOARD_LINES[1] <= mouse[0] <= BOARD_LINES[2] and BOARD_LINES[0] <= mouse[1] <= BOARD_LINES[1]:
                        return 1
                    elif BOARD_LINES[2] <= mouse[0] <= BOARD_LINES[3] and BOARD_LINES[0] <= mouse[1] <= BOARD_LINES[1]:
                        return 2
                    elif BOARD_LINES[0] <= mouse[0] <= BOARD_LINES[1] and BOARD_LINES[1] <= mouse[1] <= BOARD_LINES[2]:
                        return 3
                    elif BOARD_LINES[1] <= mouse[0] <= BOARD_LINES[2] and BOARD_LINES[1] <= mouse[1] <= BOARD_LINES[2]:
                        return 4
                    elif BOARD_LINES[2] <= mouse[0] <= BOARD_LINES[3] and BOARD_LINES[1] <= mouse[1] <= BOARD_LINES[2]:
                        return 5
                    elif BOARD_LINES[0] <= mouse[0] <= BOARD_LINES[1] and BOARD_LINES[2] <= mouse[1] <= BOARD_LINES[3]:
                        return 6
                    elif BOARD_LINES[1] <= mouse[0] <= BOARD_LINES[2] and BOARD_LINES[2] <= mouse[1] <= BOARD_LINES[3]:
                        return 7
                    elif BOARD_LINES[2] <= mouse[0] <= BOARD_LINES[3] and BOARD_LINES[2] <= mouse[1] <= BOARD_LINES[3]:
                        return 8


class Button:
    """
    A pygame button.
    
    Attributes
        - screen: :class:`pygame.display` – the screen to draw it to
        - colour: :class:`tuple[int, int, int]` – the button colour
        - hover_colour: :class:`tuple[int, int, int]` – the button colour on hover and click
        - border: :class:`int` – the border width when clicked
        - top: :class:`int` – the top y-coordinate
        - bottom: :class:`int` – the bottom y-coordinate
        - left: :class:`int` – the left x-coordinate
        - right: :class:`int` – the left x-coordinate
        - message: :class:`str` – the button's text
        - clicked: :class:`bool` – whether the button is currently selected/clicked
    """
    def __init__(self, screen, colour: tuple[int, int, int], hover_colour: tuple[int, int, int],
                 x: int, y: int, message: str):
        """
        A pygame button.
        
        :param screen: the screen to draw it to
        :param colour: the button colour
        :param hover_colour: the button colour on hover and click
        :param x: the top left x-coordinate
        :param y: the top left y-coordinate
        :param message: the button's text
        """
        self.screen = screen
        self.colour = colour
        self.hover_colour = hover_colour
        self.message = message
        self.top = y
        self.bottom = None
        self.left = x
        self.right = None
        self.border = 3
        self.clicked = False
        self.draw_button(False, False)

    def draw_button(self, hover: bool, clicked: bool):
        """
        Draw the button
        
        :param hover: whether the button is currently hovered over
        :param clicked: whether the button is currently clicked/selected
        """
        text_surface = SMALL_FONT.render(self.message, True, BLACK)
        text_rect = text_surface.get_rect()
        self.bottom = self.top + text_rect.h + 20
        self.right = self.left + text_rect.w + 40
        colour = self.colour if hover is False else self.hover_colour
        btn = pygame.draw.rect(screen, colour, (self.left, self.top, text_rect.w + 40, text_rect.h + 20))
        self.clicked = clicked
        border_colour = WHITE if clicked is False else BLACK
        pygame.draw.rect(screen, border_colour, (self.left - self.border, self.top - self.border,
                                                 text_rect.w + 40 + 2 * self.border,
                                                 text_rect.h + 20 + 2 * self.border), self.border)
        text_rect.center = btn.center
        screen.blit(text_surface, text_rect.topleft)
        
    def on_button(self, mouse) -> bool:
        """Return true if the mouse is over the button, False otherwise."""
        if self.left <= mouse[0] <= self.right and self.top <= mouse[1] <= self.bottom:
            return True
        return False
    
    def hover_on(self, mouse):
        """Change the button colour if the button is currently hovered over."""
        if self.clicked is False:
            if self.on_button(mouse):
                self.draw_button(True, False)
            else:
                self.draw_button(False, False)


def choose_type(message, tile_type: str, name: str) -> Player:
    """Let the player choose multiplayer or the AI they want to play against."""
    if message == 'Multiplayer':
        return Human(tile_type, name)
    elif message == 'Easy':
        return Random(tile_type, name)
    elif message == 'Intermediate':
        return RandomNotStupid(tile_type, name)
    else:
        return Impossible(tile_type, name)


class Game(object):
    """
    A game of tic-tac-toe.
    
    Attributes:
        board: a representation of the tic-tac-toe board
        available: a set of all available moves
        player1: a Player of the game
        player2: another Player of the game
        curr_player: the Player whose turn it is currently
    """

    def __init__(self):
        self.board = [f"{i}" for i in range(9)]
        self.available = {i for i in range(9)}
        self.player1 = Human('X', 'Human')
        mode, goes_first = game_options()
        self.player2 = choose_type(mode, 'O', 'Player 2')
        self.player1.has_first_turn = goes_first
        self.player2.has_first_turn = not self.player1.has_first_turn
        self.curr_player = self.player1 if self.player1.has_first_turn is True else self.player2

    def get_other_player(self):
        return self.player1 if self.curr_player is self.player2 else self.player2

    def validate_move(self, move: int) -> bool:
        """Make a move if it's an available square."""
        if move in self.available:
            self.available.remove(move)
            self.curr_player.all_moves.append(move)
            return True
        return False

    def play_game(self):
        """Plays a game of tic-tac-toe."""
        paint_board()
        pygame.display.update()
        moves = 0
        while moves < 9:
            #print(f"{self.curr_player.name}'s turn:")
            if not isinstance(self.curr_player, Human):
                pygame.time.delay(500)
            move = self.curr_player.move(self.curr_player.has_first_turn, self.available,
                                         self.get_other_player().all_moves)
            self.board[move] = self.curr_player.tile_type
            if self.validate_move(move) is False:
                continue
            paint_marker(self.curr_player.tile_type, move)
            pygame.display.update()
            if self.curr_player.check_winning_move(move) is True:
                end_screen(f"{self.curr_player.name} won!!")
                return 'win'
            moves += 1
            self.curr_player = self.get_other_player()
        if moves == 9:
            end_screen('It\'s a tie')
            return 'tie'


def button_row(screen, x: int, y: int, colour: tuple[int, int, int],
               hover_colour: tuple[int, int, int], text_list: list[str]) -> list[Button]:
    """
    Create, draw, and return a row of buttons.
    
    :param screen: the screen to draw them to
    :param x: the x-coordinate to start the row of buttons on
    :param y: the top y-coordinate to put the row on
    :param colour: button colour
    :param hover_colour: button colour on hover
    :param text_list: list of text to write on the buttons from left to right.
    """
    btns = []
    for text in text_list:
        btn = Button(screen, colour, hover_colour, x, y, text)
        x = btn.right + 50
        btns.append(btn)
    return btns


def click_btn_row(mouse, btn_list: list[Button], var: str) -> str:
    """Click a radio type button in a row, then un-click the rest of the buttons."""
    for btn in btn_list:
        if btn.on_button(mouse):
            btn.draw_button(True, True)
            var = btn.message
            for btn2 in btn_list:
                if btn2 is not btn:
                    btn2.draw_button(False, False)
    return var
    

def game_options():
    """Game options screen. Get the type of opponent and whether player 1 wants to go first."""
    screen.fill(WHITE)
    mode_buttons = button_row(screen, 30, 150, TEAL, DARK_TEAL, ['Multiplayer', 'Easy', 'Intermediate', 'Impossible'])
    turn_buttons = button_row(screen, 30, 300, TEAL, DARK_TEAL, ['Go First', 'Go Second'])
    turn_buttons[0].draw_button(True, True)
    start = Button(screen, GREEN, DARK_GREEN, 350, 450, 'Start')
    all_buttons = mode_buttons + turn_buttons + [start]
    
    mode = ''
    goes_first = 'Go First'

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #check for button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mode = click_btn_row(mouse, mode_buttons, mode)
                goes_first = click_btn_row(mouse, turn_buttons, goes_first)
                if start.on_button(mouse) and mode != '':
                    return mode, True if goes_first == 'Go First' else False
            #change colour of button if hovering it
            for btn in all_buttons:
                btn.hover_on(mouse)
        pygame.display.update()


def paint_board():
    """Draw the tic-tac-toe board."""
    screen.fill(WHITE)
    pygame.draw.line(screen, BLACK, (BOARD_LINES[1], BOARD_LINES[0]), (BOARD_LINES[1], BOARD_LINES[3]), 5)
    pygame.draw.line(screen, BLACK, (BOARD_LINES[2], BOARD_LINES[0]), (BOARD_LINES[2], BOARD_LINES[3]), 5)
    pygame.draw.line(screen, BLACK, (BOARD_LINES[0], BOARD_LINES[1]), (BOARD_LINES[3], BOARD_LINES[1]), 5)
    pygame.draw.line(screen, BLACK, (BOARD_LINES[0], BOARD_LINES[2]), (BOARD_LINES[3], BOARD_LINES[2]), 5)


def get_x(square: int) -> int:
    """Return the x-coordinate based on the square."""
    if square == 0 or square == 3 or square == 6:
        return BOARD_LINES[0] + 25
    elif square == 1 or square == 4 or square == 7:
        return BOARD_LINES[1] + 25
    else:
        return BOARD_LINES[2] + 25


def get_y(square: int) -> int:
    """Return the y-coordinate based on the square."""
    if square == 0 or square == 1 or square == 2:
        return BOARD_LINES[0] + 25
    elif square == 3 or square == 4 or square == 5:
        return BOARD_LINES[1] + 25
    else:
        return BOARD_LINES[2] + 25


def paint_marker(tile_type: str, square: int):
    """Draw the tile marker on the square."""
    x = get_x(square)
    y = get_y(square)
    if tile_type == 'X':
        pygame.draw.line(screen, BLACK, (x, y), (x + 100, y + 100), 10)
        pygame.draw.line(screen, BLACK, (x, y + 100), (x + 100, y), 10)
    else:
        pygame.draw.circle(screen, BLACK, (x + 50, y + 50), 50, width=7)
    
    
def game_loop():
    """Play the game until the user quits."""
    while True:
        g = Game()
        g.play_game()

        play_again = False
        again = Button(screen, GREEN, DARK_GREEN, 600, 150, "Play Again")
        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                #check for button clicks
                if event.type == pygame.MOUSEBUTTONDOWN and again.on_button(mouse):
                    play_again = True
            #if clicked 'play again' button, play another game
            if play_again is True:
                break
            #change colour of button if hovering it
            again.hover_on(mouse)
            pygame.display.update()


def end_screen(end_message: str):
    """Draw the message letting the player know if there was a tie or a win."""
    text_surface = END_FONT.render(end_message, True, PURPLE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = pygame.display.get_surface().get_rect().centerx
    text_rect.centery = 30
    screen.blit(text_surface, text_rect.topleft)
    pygame.display.update()


if __name__ == '__main__':
    game_loop()
