import copy
import random
from pickle import load, dump
from os import getcwd
from datetime import datetime


class MiniMaxComputerPlayer:

    def __init__(self, symbol, target, evaluation_function, pruning, beam_width=3, beam_search=None, change=True):
        self.symbol = symbol
        self.target = target
        self.evaluation_function = evaluation_function
        self.ab_pruning = pruning
        self.move_pruning = beam_search
        self.beam_width = beam_width
        self.lookup = None
        self.trans_table = None
        self.read_trans_table(getcwd() + '/player1/trans_table.pickle')
        self.read_lookup(getcwd() + '/player1/lookup.pickle')
        print(len(self.trans_table))
        self.change_depth = change

    def get_move(self, board):
        possible_moves = board.calc_valid_moves(self.symbol)
        if self.move_pruning is not None:
            possible_moves = self.move_pruning(board, possible_moves, self.symbol, beam_width=self.beam_width)
        random.shuffle(possible_moves)
        best_move = possible_moves[0]
        best_score = float('-inf')
        start = datetime.utcnow()
        for move in possible_moves:
            bc = copy.deepcopy(board)
            bc.make_move(self.symbol, move)
            score = self.minimax(bc, 1, False, float('-inf'), float('inf'))

            if score > best_score:
                best_score = score
                best_move = move
        end = (datetime.utcnow() - start).total_seconds()
        if end > 2.6 and self.change_depth:
            print("Whoops, changing depth for ", self.symbol)
            self.target -= 1
            print(self.target)
        elif end < 1 and self.target < 8 and self.change_depth:
            print("Going Deeper", self.symbol)
            self.target += 1


        return best_move

    def minimax(self, board, depth, max_turn, alpha, beta):
        '''
        Starts the recursive minimax algorithm and acts as the first Max move
        :param board: the board being played on
        :return: the number pair that represents the best move that can be made, determined by the algorithm
        '''
        opp = board.get_opponent_symbol(self.symbol)
        if depth == self.target or not board.game_continues():
            h = self.hash(board)
            s = self.trans_table.get(h)
            if s is not None:
                return s
            else:
                s = self.evaluation_function(board, self.symbol)
                self.trans_table[h] = s
                return s

        if self.move_pruning is not None:
            possible_moves = self.move_pruning(board, board.calc_valid_moves(self.symbol),self.symbol, beam_width=self.beam_width) \
                if max_turn else self.move_pruning(board, board.calc_valid_moves(opp), opp, beam_width=self.beam_width)
        else:
            possible_moves = board.calc_valid_moves(self.symbol) if max_turn else board.calc_valid_moves(opp)
        random.shuffle(possible_moves)

        best_score = float('-inf') if max_turn else float('inf')

        for move in possible_moves:
            bc = copy.deepcopy(board)
            bc.make_move(self.symbol, move) if max_turn else bc.make_move(bc.get_opponent_symbol(self.symbol), move)

            score = self.minimax(bc, depth+1, not max_turn, alpha, beta)

            if max_turn and score > best_score:
                best_score = score

                if self.ab_pruning:
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break

            if not max_turn and score < best_score:
                best_score = score

                if self.ab_pruning:
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break

        return best_score

    def order_moves(self, board, max_turn):
        opp = board.get_opponent_symbol(self.symbol)
        if self.move_pruning is not None:
            possible_moves = self.move_pruning(board, board.calc_valid_moves(self.symbol), self.symbol) if max_turn else self.move_pruning(board, board.calc_valid_moves(opp), opp)
        else:
            possible_moves = board.calc_valid_moves(self.symbol) if max_turn else board.calc_valid_moves(opp)
        move_scores = []
        for move in possible_moves:
            bc = copy.deepcopy(board)
            bc.make_move(self.symbol, move) if max_turn else bc.make_move(opp, move)
            h = self.hash(bc)
            s = self.trans_table.get(h)
            if s is not None:
                score = s if max_turn else -s
            else:
                s = self.evaluation_function(bc, self.symbol)
                self.trans_table[h] = s
                score = s if max_turn else -s
            move_scores.append({'move': move, 'score': score})

        ordered = sorted(move_scores, key=lambda x: x['score'], reverse=True if max_turn else False)
        return [x['move'] for x in ordered]

    @staticmethod
    def random_bitstring(length):
        return random.randint(0, 2**length - 1)

    @staticmethod
    def init_lookup(size):
        table = {}
        for x in range(size):
            for y in range(size):
                for s in range(2):
                    table[(x, y, s)] = MiniMaxComputerPlayer.random_bitstring(64)
        return table

    def hash(self, board):
        size = board.get_size()
        h = 0
        for x in range(size):
            for y in range(size):
                symbol = board.get_symbol_for_position([x, y])
                if symbol != ' ':
                    s = symbol == 'x'
                    h ^= self.lookup[(x, y, s)]
        return h

    def read_trans_table(self, path):
        try:
            with open(path, 'rb') as f:
                self.trans_table = load(f)
        except OSError:
            print("No such file or directory")
            self.trans_table = {}

    def read_lookup(self, path):
        try:
            with open(path, 'rb') as f:
                self.lookup = load(f)
        except OSError:
            print("No such file or directory")
            self.lookup = self.init_lookup(8)

    def write_tras_lookup(self, trans_path, lookup_path):
        with open(trans_path, 'wb') as f:
            dump(self.trans_table, f)
        with open(lookup_path, 'wb') as f:
            dump(self.lookup, f)


def simple_evaluate(board, symbol):
    scores = board.calc_scores()
    opp = board.get_opponent_symbol(symbol)
    if scores[symbol] > scores[opp]:
        return scores[symbol]
    elif scores[symbol] == scores[opp]:
        return 0
    else:
        return -scores[opp]


def difference_heuristic(board, symbol):
    scores = board.calc_scores()
    opponent = board.get_opponent_symbol(symbol)

    point_percent = 100 * ((scores[symbol] - scores[opponent]) / (scores[symbol] + scores[opponent]))
    return point_percent


def mobility_heuristic(board, symbol):
    opponent = board.get_opponent_symbol(symbol)

    if board.game_continues():
        num_moves = len(board.calc_valid_moves(symbol))
        num_opponent_moves = len(board.calc_valid_moves(opponent))

        percent_mobility = 100 * ((num_moves - num_opponent_moves) / (num_moves + num_opponent_moves))
        return percent_mobility

    else:
        return 0


def corner_heuristic(board, symbol):
    opponent = board.get_opponent_symbol(symbol)
    size = board.get_size()
    corners = [[0, 0], [0, size-1], [size-1, 0], [size-1, size-1]]
    self_corners = 0
    opponent_corners = 0

    for corner in corners:
        if board.get_symbol_for_position(corner) == symbol:
            self_corners += 1
        elif board.get_symbol_for_position(corner) == opponent:
            opponent_corners += 1

    if self_corners + opponent_corners != 0:
        percent_corners = 100 * ((self_corners - opponent_corners) / (self_corners + opponent_corners))
        return percent_corners
    else:
        return 0


def combined_heuristics(board, symbol):
    overall_heuristic = difference_heuristic(board, symbol) + mobility_heuristic(board, symbol) + corner_heuristic(board, symbol)
    return overall_heuristic
