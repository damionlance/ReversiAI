import copy
from player1.damionWork import BeamSearch


class MiniMaxComputerPlayer:

    def __init__(self, symbol, target, evaluation_function):
        self.symbol = symbol
        self.target = target
        self.evaluation_function = evaluation_function

    def get_move(self, board):
        return self.minimax(board)

    def minimax(self, board):
        '''
        Starts the recursive minimax algorithm and acts as the first Max move
        :param board: the board being played on
        :return: the number pair that represents the best move that can be made, determined by the algorithm
        '''
        possible_moves = board.calc_valid_moves(self.symbol)
        best_move = possible_moves[0]
        best_score = float('-inf')
        for move in possible_moves:
            bc = copy.deepcopy(board)
            bc.make_move(self.symbol, move)
            # Find min score and increment depth by 1
            score = self.min_play(bc, 1)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def min_play(self, board, depth):
        '''
        acts as the opponent in the minimax algorithm
        :param board: board being played on
        :param depth: current move depth
        :return: the minimum score that can be found
        '''
        # Recursive base case: target depth is met or game is over
        if depth == self.target or not board.game_continues():
            return self.evaluation_function(board, self.symbol)

        sym = board.get_opponent_symbol(self.symbol)
        possible_moves = board.calc_valid_moves(sym)
        best_score = float('inf')
        for move in possible_moves:
            bc = copy.deepcopy(board)
            bc.make_move(sym, move)
            score = self.max_play(bc, depth+1)
            if score < best_score:
                best_move = move
                best_score = score
        return best_score

    def max_play(self, board, depth):
        '''
        acts as the player in the minimax algorithm
        :param board: board being played on
        :param depth: current move depth
        :return: the max score that can be found
        '''
        if depth == self.target or not board.game_continues():
            return self.evaluation_function(board, self.symbol)

        possible_moves = board.calc_valid_moves(self.symbol)
        best_score = float('-inf')
        for move in possible_moves:
            bc = copy.deepcopy(board)
            bc.make_move(self.symbol, move)
            score = self.min_play(bc, depth+1)
            if score > best_score:
                best_move = move
                best_score = score
        return best_score


def simple_evaluate(board, symbol):
    scores = board.calc_scores()
    opp = board.get_opponent_symbol(symbol)
    if scores[symbol] > scores[opp]:
        return scores[symbol] - scores[opp]
    elif scores[symbol] == scores[opp]:
        return 0
    else:
        return -1
