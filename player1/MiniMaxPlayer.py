import copy
import random


class MiniMaxComputerPlayer:

    def __init__(self, symbol, target, evaluation_function,):
        self.symbol = symbol
        self.target = target
        self.evaluation_function = evaluation_function

    def get_move(self, board):
        possible_moves = board.calc_valid_moves(self.symbol)
        random.shuffle(possible_moves)
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
        random.shuffle(possible_moves)

        best_score = float('-inf') if max_turn else float('inf')

        for move in possible_moves:
            bc = copy.deepcopy(board)
            bc.make_move(self.symbol, move) if max_turn else bc.make_move(bc.get_opponent_symbol(self.symbol), move)

            score = self.minimax(bc, depth+1, not max_turn, alpha, beta)

            if max_turn and score > best_score:
                best_score = score
                best_move = move

            if not max_turn and score < best_score:
                best_score = score

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
    if scores[symbol] > scores[opp]:
        return scores[symbol] - scores[opp]
    elif scores[symbol] == scores[opp]:
        return 0
    else:
        return -1
