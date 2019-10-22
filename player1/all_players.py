from player1.MiniMaxPlayer import MiniMaxComputerPlayer, simple_evaluate, difference_heuristic, combined_heuristics


def get_default_player(symbol):
    """
    :returns: a default minimax player that can operate successfully on a given 8x8 board
    """

    return MiniMaxComputerPlayer(symbol, 3, difference_heuristic, pruning=False)


def get_player_pruning(symbol):
    """
    :Tim Clerico:
    :Alpha Beta Pruning:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MiniMaxComputerPlayer(symbol, 3, difference_heuristic, pruning=True)


def get_player_heuristic(symbol):
    """
    :Sean McQuilan:
    :Better Heuristics:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MiniMaxComputerPlayer(symbol, 3, combined_heuristics, pruning=False)


def get_player_beam(symbol):
    """
    :Damion Lance:
    :Beam Search:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    pass


def get_player_d(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    pass


def get_combined_player(symbol):
    """
    :returns: the best combination of the minimax enhancements that your team can create
    """
    return MiniMaxComputerPlayer(symbol, 3, combined_heuristics, pruning=True)
