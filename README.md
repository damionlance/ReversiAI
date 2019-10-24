# ReversiAI

### 1. Alpha Beta Pruning

The implementation of Alpha Beta Pruning that was devised for this project is more time efficient than the base MiniMax agent without losing out on the effect on gameplay. When both agents are setup to only search down to the same depth, the agent with Alpha Beta Pruning always completes it's moves quicker. This allows it to look down at further depths of the decision tree and preform better than the base minimax agent.

With the search depth set at 4 I found that the Alpha Beta Agent made its decisions for each move more than twice as fast as the base agent with an average decision time of 0.2 seconds while the base agent had an average of 0.56 seconds.



### 2. Beam Search

We implemented a Beam Search algorithm to try and increase speed of search. This allows us to increase depth or to use more intensive algorithms without sacrificing speed because we are trimming improbable routes. With just beam search, on every turn decision cycle, we found our algorithm to be significantly faster than it's counter part without beam search. However, with just beam search and none of our other enhancements we tend to lose more games. This is expected as beam search cuts branches by guessing and doesn't play perfectly.

Given two agents running the same depth here is the speed difference we see:

{'X': 17, 'O': 3, 'TIE': 0}

{'X': 143.83176200000003, 'O': 21.853547}

Note that we expect O to lose more because both agents search the same depth

### 3. Improved Hueristics

To implement a better heuristic than a simple greedy one, I looked into the most important aspects of any Reversi move. There are four aspects to think of for any given move that one should consider:

Coin Parity: This is the difference in the number of pieces that you and your opponent have on the board (basically the previously mentioned greedy heuristic).

Mobility: This prioritizes giving you a high number of moves, while limiting the numebr of moves your opponent has.

Corners: Self explanatory; this heuristic prioritizes getting control of the corners, as corner pieces are extremely valuable in a Reversi game.

Stability: The stability of a piece means how likely it is to be overturned in the next turn. It can be stable, semi-stable, or unstable.

I was able to get 3 of the 4 working within good time, as I was not able to find of a way to implement a stability check while keeping the agent fast. However, this does not matter too much as the combination of the other 3 factors make the overall MiniMax agent significantly more efficient. While it did not make the agent more time efficient, each heuristic seemed to help win more games.

From Most to Least impactful:
Corner Heuristic - On an average of 20 games, this beats the mobility heuristic and the coin parity heuristic 15-18 games

Mobility Heuristic - This flips back and forth with the coin parity heuristic, either winning by 3-4 or losing by 3-4, but it seems to be winning a small margin more

Coin Parity - The greedy heuristic means the least, as a highly greedy board state does not mean a stable one. This one loses most often to the Mobility Heuristic usually by 3-4, and the corner one usually 17-18 times out of 20.

A combination of the 3 wins against every other heuristic which is no surprise, as it just combines all previous ones. it wins 18-19 games against the mobility and coin parity heuristics, and wins 14-15 times versus the corner herustic, which just further enforces how important corners are in Reversi.



