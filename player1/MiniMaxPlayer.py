import copy


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
            score = self.max_play(bc, depth + 1)
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
            score = self.min_play(bc, depth + 1)
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


