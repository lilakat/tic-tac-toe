from TicTacToeText import Human, Impossible, Player, Random, RandomNotStupid


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
        self.player1 = Impossible('X', 'Impossible')
        self.player2 = Impossible('O', 'Impossible2')
        self.player1.has_first_turn = True
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
        #print(self)
        moves = 0
        while moves < 9:
            #print(f"{self.curr_player.name}'s turn:")
            move = self.curr_player.move(self.curr_player.has_first_turn, self.available,
                                         self.get_other_player().all_moves)
            self.board[move] = self.curr_player.tile_type
            if self.validate_move(move) is False:
                print('Try again, that\'s not an available move')
                continue
            #print(self)
            if self.curr_player.check_winning_move(move) is True:
                #print(f"{self.curr_player.name} won!!")
                return 'win'
            moves += 1
            self.curr_player = self.get_other_player()
        if moves == 9:
            #print('It\'s a tie')
            return 'tie'


def game_loop():
    play_again = 1000000
    num_ties = 0
    num_player1_wins = 0
    num_player2_wins = 0
    while play_again >= 0:
        g = Game()
        if g.play_game() == 'tie':
            num_ties += 1
        elif g.curr_player is g.player1:
            num_player1_wins += 1
        else:
            num_player2_wins += 1
        play_again -= 1
    print("ties: " + str(num_ties))
    print("Player1 wins: " + str(num_player1_wins))
    print("Player2 wins: " + str(num_player2_wins))


if __name__ == '__main__':
    game_loop()
