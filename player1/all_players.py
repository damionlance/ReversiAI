from player1.MiniMaxPlayer import MiniMaxComputerPlayer, simple_evaluate, difference_heuristic, combined_heuristics
from player1.damionWork.BeamSearch import beam_search


def get_default_player(symbol, depth):
    """
    :returns: a default minimax player that can operate successfully on a given 8x8 board
    """

    return MiniMaxComputerPlayer(symbol, depth, difference_heuristic, pruning=False)


def get_player_pruning(symbol, depth):
    """
    :Tim Clerico:
    :Alpha Beta Pruning:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MiniMaxComputerPlayer(symbol, depth, difference_heuristic, pruning=True)


def get_player_heuristic(symbol, depth):
    """
    :Sean McQuilan:
    :Better Heuristics:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MiniMaxComputerPlayer(symbol, depth, combined_heuristics, pruning=False)


def get_player_beam(symbol, depth):
    """
    :Damion Lance:
    :Beam Search:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MiniMaxComputerPlayer(symbol, depth, combined_heuristics, pruning=False, beam_search=beam_search)


def get_player_d(symbol,depth):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    pass


def get_combined_player(symbol, depth):
    """
    :returns: the best combination of the minimax enhancements that your team can create
    """
    return MiniMaxComputerPlayer(symbol, depth, combined_heuristics, pruning=True, beam_search=beam_search)
