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


