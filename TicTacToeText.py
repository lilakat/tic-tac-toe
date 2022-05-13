from abc import abstractmethod
import random


lines = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8},
         {0, 3, 6}, {1, 4, 7}, {2, 5, 8},
         {0, 4, 8}, {2, 4, 6}]

corners = [0, 2, 6, 8]


def get_corner(move: int) -> int:
    if move == 0:
        return 8
    elif move == 2:
        return 6
    elif move == 6:
        return 2
    elif move == 8:
        return 0


def get_opposite(move: int) -> int:
    if move == 1:
        return 7
    elif move == 3:
        return 5
    elif move == 5:
        return 3
    elif move == 7:
        return 1


def check_if_losing(available: set, other_player_moves: list) -> int | None:
    for line in lines:
        if len(line & set(other_player_moves)) >= 2:
            possible_moves = line & available
            if len(possible_moves) == 1:
                return possible_moves.pop()
    return False


class Player:
    """
    An abstract player.

    Attributes
        - tile_type: :class:`str` – which marker this player puts down
        - name: :class:`str` – the name of this player
        - all_moves: :class:`list[int]` – all moves this player has made
        - has_first_turn: :class:`bool` – whether this player goes first
    """

    @abstractmethod
    def __init__(self, tile_type: str, name: str):
        """
        :param tile_type: which marker this player puts down
        :param name: the name of this player
        """
        self.tile_type = tile_type
        self.name = name
        self.all_moves = []
        self.has_first_turn = None

    @abstractmethod
    def move(self, has_first_turn: bool, available: set, other_player_moves: list) -> int:
        """Returns a valid move."""
        pass

    def check_winning_move(self, move: int) -> bool:
        """Returns whether a move won the game."""
        for line in lines:
            if move in line and all(x in self.all_moves for x in line):
                return True
        return False


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
        while True:
            move = input("Choose an available square [0-8]")
            if move.isdigit() and int(move) < 9:
                return int(move)
            else:
                print("That's not a valid square")


class Random(Player):
    """
    An AI player that plays random moves.

    Attributes
        - tile_type: :class:`str` – which marker this player puts down
        - name: :class:`str` – the name of this player
    """

    def __init__(self, tile_type, name):
        super().__init__(tile_type, name)

    def move(self, has_first_turn: bool, available: set, other_player_moves: list) -> int:
        return random.choice(tuple(available))


class RandomNotStupid(Player):
    """
    An AI player that plays random moves but takes and blocks winning moves.

    Attributes
        - tile_type: :class:`str` – which marker this player puts down
        - name: :class:`str` – the name of this player
    """

    def __init__(self, tile_type, name):
        super().__init__(tile_type, name)

    def try_win_or_block(self, available: set, other_player_moves: list):
        possible_moves = check_if_losing(available, self.all_moves)
        if possible_moves is not False:  #check if there's any winning moves
            return possible_moves
        possible_moves = check_if_losing(available, other_player_moves)
        if possible_moves is not False:  #check if it needs to block other player
            return possible_moves

    def move(self, has_first_turn: bool, available: set, other_player_moves: list) -> int:
        win_block = self.try_win_or_block(available, other_player_moves)
        if win_block is not None:
            return win_block
        return random.choice(tuple(available))


class Impossible(RandomNotStupid):
    """
    An AI player that never loses.
    
    Attributes
        - tile_type: :class:`str` – which marker this player puts down
        - name: :class:`str` – the name of this player
        - case: :class:`str` – whether opponent put down a corner, edge, or middle on their first move
    """

    def __init__(self, tile_type, name):
        super().__init__(tile_type, name)
        self.case = None

    def goes_first_or_middle_case(self, available: set) -> int:
        """
        Move algorithm if AI goes first or if the other player's first move
        is the middle tile.
        """
        if len(self.all_moves) == 0:
            return random.choice(corners)
        elif len(self.all_moves) == 1:
            corner = get_corner(self.all_moves[0])
            if corner in available:
                return corner
            else:
                return random.choice(tuple(set(corners) & available))
        elif len(self.all_moves) == 2:
            corner = random.choice(tuple(set(corners) & available))
            if corner is not None:
                return corner
        return random.choice(tuple(available))

    def corner_case(self, available: set, other_player_moves: list) -> int:
        """
        Move algorithm for if AI goes 2nd and other player picks a corner on first turn.
        Steps are:
        1. pick middle
        2. pick an edge to force them to block
            (so if they chose an edge on their second turn, don't pick the edge opposite to that)
        3. pick a corner beside their block
        """
        if len(self.all_moves) == 0:
            return 4
        elif len(self.all_moves) == 1:
            edges = {1, 3, 5, 7}
            if other_player_moves[1] in edges:
                opposite = get_opposite(other_player_moves[1])
                edges.remove(opposite)
            return random.choice(tuple(edges & available))
        elif len(self.all_moves) == 2:
            if other_player_moves[2] == 1 and len(tuple({0, 2} & available)) != 0:
                return random.choice(tuple({0, 2} & available))
            elif other_player_moves[2] == 3 and len(tuple({0, 6} & available)) != 0:
                return random.choice(tuple({0, 6} & available))
            elif other_player_moves[2] == 5 and len(tuple({2, 8} & available)) != 0:
                return random.choice(tuple({2, 8} & available))
            elif other_player_moves[2] == 7 and len(tuple({6, 8} & available)) != 0:
                return random.choice(tuple({6, 8} & available))
        return random.choice(tuple(available))

    def edge_case(self, available: set, other_player_moves: list) -> int:
        """
        Move algorithm for if AI goes 2nd and other player picks an edge on the first turn.
        Steps are:
        1. pick a corner next to their first move
        2. pick another corner, on the same side as the first one, but not on the same side as their
        first move - to force them to block
        3. pick the middle
        """
        if len(self.all_moves) == 0:
            if other_player_moves[0] == 1:
                return random.choice([0, 2])
            elif other_player_moves[0] == 3:
                return random.choice([0, 6])
            elif other_player_moves[0] == 5:
                return random.choice([2, 8])
            else:
                return random.choice([6, 8])
        elif len(self.all_moves) == 1:
            if 0 in self.all_moves:
                if 1 not in other_player_moves and 2 in available:
                    return 2
                elif 3 not in other_player_moves and 6 in available:
                    return 6
            elif 2 in self.all_moves:
                if 1 not in other_player_moves and 0 in available:
                    return 0
                elif 5 not in other_player_moves and 8 in available:
                    return 8
            elif 6 in self.all_moves:
                if 7 not in other_player_moves and 8 in available:
                    return 8
                elif 3 not in other_player_moves and 0 in available:
                    return 0
            elif 8 in self.all_moves:
                if 7 not in other_player_moves and 6 in available:
                    return 6
                elif 5 not in other_player_moves and 2 in available:
                    return 2
            return 4
        elif len(self.all_moves) == 2:
            if 4 in available:
                return 4
        return random.choice(tuple(available))

    def goes_second(self, available: set, other_player_moves: list) -> int:
        """
        Identify which algorithm to use depending on what the other player's
        first move was, and return a move based on that.
        """
        #first move - identify which case
        if len(self.all_moves) == 0:
            if other_player_moves[0] in corners:
                self.case = 'corner'
            elif other_player_moves[0] in [1, 3, 5, 7]:
                self.case = 'edge'
            else:
                self.case = 'middle'
        #go to algorithm for the case
        if self.case == 'corner':
            return self.corner_case(available, other_player_moves)
        elif self.case == 'edge':
            return self.edge_case(available, other_player_moves)
        else:
            return self.goes_first_or_middle_case(available)

    def move(self, has_first_turn: bool, available: set, other_player_moves: list) -> int:
        """
        Return a valid move for Impossible AI.
        """
        win_block = self.try_win_or_block(available, other_player_moves)
        if win_block is not None:
            return win_block
        if has_first_turn is True:
            return self.goes_first_or_middle_case(available)
        else:
            return self.goes_second(available, other_player_moves)


def choose_type(tile_type: str, name: str) -> Player:
    """Let the player choose multiplayer or the AI they want to play against."""
    choice = input("2 player [H] or single player [options: Easy[E], Intermediate[M], or Impossible[I]]?").lower()
    if choice == 'h':
        return Human(tile_type, name)
    elif choice == 'e':
        return Random(tile_type, name)
    elif choice == 'm':
        return RandomNotStupid(tile_type, name)
    else:
        return Impossible(tile_type, name)


class Game(object):
    """
    A game of tic-tac-toe.
    
    Attributes
        - board: :class:`list[str]` – a representation of the tic-tac-toe board
        - available: :class:`list[int]` – a set of all available moves
        - player1: :class:`Player` – a Player of the game
        - player2: :class:`Player` – another Player of the game
        - curr_player: :class:`Player` – the Player whose turn it is currently
    """

    def __init__(self):
        self.board = [f"{i}" for i in range(9)]
        self.available = {i for i in range(9)}
        self.player1 = Human('X', 'Human')
        self.player2 = choose_type('O', 'Player 2')
        self.player1.has_first_turn = True if input("Do you want to go first? [T/F]").lower() == 't' else False
        self.player2.has_first_turn = not self.player1.has_first_turn
        self.curr_player = self.player1 if self.player1.has_first_turn is True else self.player2

    def __str__(self):
        s = ""
        i = 0
        for j in range(3):
            s += self.board[i] + " | " + self.board[i + 1] + " | " + self.board[i + 2] + "\n"
            if not j == 2:
                s += "----------\n"
            i += 3
        return s

    def get_other_player(self):
        """Return the player whose turn is next."""
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
        print(self)
        moves = 0
        while moves < 9:
            print(f"{self.curr_player.name}'s turn:")
            move = self.curr_player.move(self.curr_player.has_first_turn, self.available,
                                         self.get_other_player().all_moves)
            self.board[move] = self.curr_player.tile_type
            if self.validate_move(move) is False:
                print('Try again, that\'s not an available move')
                continue
            print(self)
            if self.curr_player.check_winning_move(move) is True:
                print(f"{self.curr_player.name} won!!")
                return 'win'
            moves += 1
            self.curr_player = self.get_other_player()
        if moves == 9:
            print('It\'s a tie')
            return 'tie'


def game_loop():
    """Play tic-tac-toe in a loop until the player quits."""
    play_again = True
    num_ties = 0
    num_player1_wins = 0
    num_player2_wins = 0
    while play_again is True:
        g = Game()
        g.play_game()
        if g == 'tie':
            num_ties += 1
        elif g.curr_player is g.player1:
            num_player1_wins += 1
        else:
            num_player2_wins += 1
        again = input("do you want to play again? [Y/N]")
        if again.lower() != 'y':
            print('Thanks for playing!')
            
            break


if __name__ == '__main__':
    game_loop()
