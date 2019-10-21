import copy

def beam_search(board, move_list, symbol, beam_width=4):
    value_dictionary = {}
    for move in move_list:
        tempboard = copy.deepcopy(board)
        tempboard.make_move(symbol, move)
        value_dictionary[tuple(move)] = _heuristic_score(tempboard, symbol, _valued_corners_edges())
    modified_move_list = []
    for i in range(beam_width):
        if len(value_dictionary) == 0:
            break
        max_value = max(value_dictionary.values())
        max_keys = [k for k, v in value_dictionary.items() if v == max_value]
        modified_move_list.append(max_keys[0])
        value_dictionary.pop(max_keys[0])
    return modified_move_list

def _heuristic_score(board, symbol, heuristic_function):
    score = 0
    for x in range(board.get_size()):
        for y in range(board.get_size()):
            if board.get_symbol_for_position([x, y]) == symbol:
                score += heuristic_function[x][y]
    return score

def _valued_corners_edges():
    compareBoard = [[100, 25, 25, 25, 25, 25, 25, 100],
                    [25, 1, 1, 1, 1, 1, 1, 25],
                    [25, 1, 1, 1, 1, 1, 1, 25],
                    [25, 1, 1, 1, 1, 1, 1, 25],
                    [25, 1, 1, 1, 1, 1, 1, 25],
                    [25, 1, 1, 1, 1, 1, 1, 25],
                    [25, 1, 1, 1, 1, 1, 1, 25],
                    [100, 25, 25, 25, 25, 25, 25, 100]]
    return compareBoard

def _gradually_valued_corners_edges():
    compareBoard = [[100, 25, 25, 25, 25, 25, 25, 100],
                    [25, 10, 10, 10, 10, 10, 10, 25],
                    [25, 10, 5, 5, 5, 5, 10, 25],
                    [25, 10, 5, 1, 1, 5, 10, 25],
                    [25, 10, 5, 1, 1, 5, 10, 25],
                    [25, 10, 5, 5, 5, 5, 10, 25],
                    [25, 10, 10, 10, 10, 10, 10, 25],
                    [100, 25, 25, 25, 25, 25, 25, 100]]
    return compareBoard