# Written by Toby Dragon

import copy
from datetime import datetime
from reversi_board import ReversiBoard
from player1.all_players import *
from os import getcwd


class ReversiGame:

    def __init__(self, player1, player2, show_status=True, board_size=8, board_filename=None):
        self.player1 = player1
        self.player2 = player2
        self.show_status = show_status
        if board_filename is None:
            self.board = ReversiBoard(board_size)
        else:
            self.board = ReversiBoard(board_filename=board_filename)
        self.decision_times = {self.player1.symbol: 0, self.player2.symbol: 0}
        self.moves_made = {self.player1.symbol: 0, self.player2.symbol: 0}
        self.max_decision_time = {self.player1.symbol: 0, self.player2.symbol: 0}
        self.play_game()

    def play_game(self):
        if self.show_status:
            self.board.draw_board()
        while self.board.game_continues():
            self.play_round()
        if self.show_status:
            print("Game over, Final Scores:")
            print_scores(self.board.calc_scores())

    def play_round(self):
        start = datetime.now()
        self.play_move(self.player1)
        self.decision_times[self.player1.symbol] += (datetime.now()-start).total_seconds()
        move_time = (datetime.now()-start).total_seconds()
        if move_time > 2.5:
            print("BEEG MOVE",move_time)
        self.max_decision_time[self.player1.symbol] = move_time if move_time > self.max_decision_time[self.player1.symbol] else self.max_decision_time[self.player1.symbol]
        start = datetime.now()
        self.play_move(self.player2)
        self.decision_times[self.player2.symbol] += (datetime.now()-start).total_seconds()
        move_time = (datetime.now()-start).total_seconds()
        if move_time > 2.5:
            print("BEEG MOVE",move_time)
        self.max_decision_time[self.player2.symbol] = move_time if move_time > self.max_decision_time[self.player2.symbol] else self.max_decision_time[self.player2.symbol]



    def play_move(self, player):
        if self.board.calc_valid_moves(player.symbol):
            self.moves_made[player.symbol] += 1
            chosen_move = player.get_move(copy.deepcopy(self.board))
            if not self.board.make_move(player.symbol, chosen_move):
                print("Error: invalid move made")
            elif self.show_status:
                self.board.draw_board()
                print_scores(self.board.calc_scores())
        elif self.show_status:
            print(player.symbol, "can't move.")

    def calc_winner(self):
        scores = self.board.calc_scores()
        if scores[self.player1.symbol] > scores[self.player2.symbol]:
            return self.player1.symbol
        if scores[self.player1.symbol] < scores[self.player2.symbol]:
            return self.player2.symbol
        else:
            return "TIE"

    def get_decision_times(self):
        return self.decision_times


def print_scores(score_map):
    for symbol in score_map:
        print(symbol, ":", score_map[symbol], end="\t")
    print()


def compare_players(player1, player2, games):
    game_count_map = {player1.symbol: 0, player2.symbol: 0, "TIE": 0}
    time_elapsed_map = {player1.symbol: 0, player2.symbol: 0}
    average_scores = {player1.symbol: 0, player2.symbol: 0}
    average_move_time = {player1.symbol: 0, player2.symbol: 0}
    moves = {player1.symbol:0, player2.symbol:0}
    max_decision_time = {player1.symbol: 0, player2.symbol: 0}
    for i in range(0, games):
        if i % 2 == 0:
            print(i, "games finished")
        if i % 2 == 0:
            game = ReversiGame(player1, player2, show_status=False, board_size=8)
        else:
            game = ReversiGame(player2, player1, show_status=False, board_size=8)

        #print(player1.turn_number)

        game_count_map[game.calc_winner()] += 1
        decision_times = game.get_decision_times()
        average_scores[player1.symbol] += game.board.calc_scores()[player1.symbol]
        average_scores[player2.symbol] += game.board.calc_scores()[player2.symbol]

        max_decision_time[player1.symbol] = game.max_decision_time[player1.symbol] if game.max_decision_time[player1.symbol] > max_decision_time[player1.symbol] else max_decision_time[player1.symbol]
        max_decision_time[player2.symbol] = game.max_decision_time[player2.symbol] if game.max_decision_time[player2.symbol] > max_decision_time[player2.symbol] else max_decision_time[player2.symbol]

        for symbol in decision_times:
            time_elapsed_map[symbol] += decision_times[symbol]
            average_move_time[symbol] += (decision_times[symbol] / game.moves_made[symbol])
            moves[symbol] += game.moves_made[symbol]

        player2.write_tras_lookup(getcwd() + '/player1/trans_table.pickle', getcwd() + '/player1/lookup.pickle')

    average_scores[player1.symbol] = average_scores[player1.symbol]/games
    average_scores[player2.symbol] = average_scores[player2.symbol]/games
    print(game_count_map)
    print(average_scores)
    for symbol in ["X", 'O']:
        t = time_elapsed_map[symbol] / moves[symbol]
        print(symbol+" average decision time: ", t)

    print("Highest Decision Times: ", max_decision_time)


def main():
    player1 = get_combined_player('X', depth=7)
    player2 = get_base_player('O', depth=3)
    game = ReversiGame(player1, player2, show_status=True)
    print(game.max_decision_time)
    print("Total Moves made by each player: "+ "X: "+ str(game.moves_made['X']) + " O: "+str(game.moves_made['O']))
    for player in ['X', 'O']:
        moves = game.moves_made[player]
        time = game.decision_times[player]
        average = time/moves
        print("Average Decision Time For Player "+player+": "+str(average))
    player2.write_tras_lookup(getcwd() + '/player1/trans_table.pickle', getcwd() + '/player1/lookup.pickle')

    # compare_players(player1, player2, 50)

    # once we are close to end of game widen the beam
    # print(game.max_decision_time)


if __name__ == "__main__":
    main()
