from player1.MiniMaxPlayer import MiniMaxComputerPlayer, simple_evaluate, difference_heuristic, combined_heuristics
from player1.damionWork.BeamSearch import beam_search


def get_base_player(symbol, depth=4):
    """
    :returns: a default minimax player that can operate successfully on a given 8x8 board
    """

    return MiniMaxComputerPlayer(symbol, depth, difference_heuristic, pruning=False)


def get_player_a(symbol):
    """
    :Tim Clerico:
    :Alpha Beta Pruning:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MiniMaxComputerPlayer(symbol, 4, difference_heuristic, pruning=True)


def get_player_b(symbol):
    """
    :Sean McQuilan:
    :Better Heuristics:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MiniMaxComputerPlayer(symbol, 4, combined_heuristics, pruning=False)


def get_player_c(symbol):
    """
    :Damion Lance:
    :Beam Search:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MiniMaxComputerPlayer(symbol, 5, difference_heuristic, pruning=False, beam_search=beam_search)


def get_player_d(symbol):
    """
    :Damion Lance:
    :Beam Search:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MiniMaxComputerPlayer(symbol, 5, difference_heuristic, pruning=False, beam_search=beam_search)


def get_combined_player(symbol, depth=7, width=3, expanding=True):
    """
    :returns: the best combination of the minimax enhancements that your team can create
    """
    return MiniMaxComputerPlayer(symbol, depth, combined_heuristics, pruning=True, beam_search=beam_search, beam_width=width)
