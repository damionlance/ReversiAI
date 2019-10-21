import copy
import random


class MiniMaxComputerPlayer:

    def __init__(self, symbol, target, evaluation_function, pruning):
        self.symbol = symbol
        self.target = target
        self.evaluation_function = evaluation_function
        self.ab_pruning = pruning

    def get_move(self, board):
        possible_moves = board.calc_valid_moves(self.symbol)
        # random.shuffle(possible_moves)
        best_move = possible_moves[0]
        best_score = float('-inf')
        for move in possible_moves:
            bc = copy.deepcopy(board)
            bc.make_move(self.symbol, move)

            score = self.minimax(bc, 1, False, float('-inf'), float('inf'))

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax(self, board, depth, max_turn, alpha, beta):
        '''
        Starts the recursive minimax algorithm and acts as the first Max move
        :param board: the board being played on
        :return: the number pair that represents the best move that can be made, determined by the algorithm
        '''

        if depth == self.target or not board.game_continues():
            return self.evaluation_function(board, self.symbol)

        opp = board.get_opponent_symbol(self.symbol)

        # possible_moves = self.order_moves(board, max_turn)

        possible_moves = board.calc_valid_moves(self.symbol) if max_turn else board.calc_valid_moves(opp)
        # random.shuffle(possible_moves)

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
        possible_moves = board.calc_valid_moves(self.symbol) if max_turn else board.calc_valid_moves(opp)
        move_scores = []
        for move in possible_moves:
            bc = copy.deepcopy(board)
            bc.make_move(self.symbol, move) if max_turn else bc.make_move(opp, move)
            score = self.evaluation_function(bc, self.symbol) if max_turn else self.evaluation_function(bc, opp)
            move_scores.append({'move': move, 'score':score})

        ordered = sorted(move_scores, key=lambda x: x['score'], reverse=True if max_turn else False)
        return [x['move'] for x in ordered]



def simple_evaluate(board, symbol):
    scores = board.calc_scores()
    opp = board.get_opponent_symbol(symbol)
    diff = scores[symbol] - scores[opp]
    if scores[symbol] > scores[opp]:
        return scores[symbol]
    elif scores[symbol] == scores[opp]:
        return 0
    else:
        return 0-scores[opp]


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


