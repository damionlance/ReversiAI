# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import random
import copy
from collections import deque
import heapq

class HumanPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        # Let the player type in their move.
        # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
        valid_digits = []
        for i in range(1, board.get_size()+1):
            valid_digits.append(str(i))
        no_valid_move = True
        while no_valid_move:
            move = input(self.symbol + ', enter your move:').lower()
            if len(move) == 2 and move[0] in valid_digits and move[1] in valid_digits:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if board.is_valid_move(self.symbol, ( x, y) ):
                    no_valid_move = False
                    return [x, y]
                else:
                    print('Not a valid move.')
            else:
                print('Bad input. Type valid x digit, then the y digit.')


class RandomComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        return random.choice(board.calc_valid_moves(self.symbol))


class GreedyComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    # Super simple move decision that will always make move that gives highest score
    def get_move(self, board):
        # copy.deepcopy(self.board)
        possible = board.calc_valid_moves(self.symbol)
        moves = []
        for p in possible:
            board_copy = copy.deepcopy(board)
            board_copy.make_move(symbol=self.symbol, position=p)
            score = board_copy.calc_scores()[self.symbol]
            heapq.heappush(moves, (score, p))

        to_make = moves.pop()
        return to_make[1]


class MiniMaxComputerPlayer:

    def __init__(self, symbol, target):
        self.symbol = symbol
        self.target = target

    def get_move(self, board):
        return self.minimax(board)

    def minimax(self, board):
        possible_moves = board.calc_valid_moves(self.symbol)
        best_move = possible_moves[0]
        best_score = float('-inf')
        for move in possible_moves:
            bc = copy.deepcopy(board)
            bc.make_move(self.symbol, move)
            score = self.min_play(bc, 1)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def min_play(self, board, depth):
        # base case: at target depth
        if depth == self.target or not board.game_continues():
            return self.evaluate(board)
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
        if depth == self.target or not board.game_continues():
            return self.evaluate(board)
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

    def evaluate(self, board):
        scores = board.calc_scores()
        opp = board.get_opponent_symbol(self.symbol)
        if scores[self.symbol] > scores[opp]:
            return scores[self.symbol] - scores[opp]
        elif scores[self.symbol] == scores[opp]:
            return 0
        else:
            return -1
