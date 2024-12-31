# Game Theory Tournament Simulator

This repository contains a Python script that simulates a tournament of strategies competing in a repeated prisoner's dilemma game. It features several pre-defined strategies and allows for customization of game parameters.

## Features

- Simulates multiple matches in a tournament setting.
- Includes predefined strategies: **Angel**, **Diablo**, **Tito**, **Loco**, and **Resentido**.
- Configurable game parameters:
  - `C`: Payoff for mutual cooperation.
  - `T`: Payoff for defecting when the opponent cooperates.
  - `p`: Probability of action error.
  - `allow_self_play`: Toggle self-play (default: `True`).
- Aggregates results over multiple tournament simulations.
- Outputs detailed statistics, including:
  - Payoff matrix.
  - Total scores and rankings.
  - Winners and their average scores.
  - Maximum and minimum individual gains.

## Requirements

- Python 3.x
- No external libraries are required.

## How to Use

### Running the Script

You can run the script directly from the command line. It accepts three optional arguments: `C`, `T`, and `p`.

```bash
python tournament_simulator.py [C] [T] [p]
```

- **`C`**: Cooperation payoff (default: `1`).
- **`T`**: Temptation payoff (default: `2`).
- **`p`**: Probability of error (default: `0.0`).

Example:
```bash
python tournament_simulator.py 1 2 0.1
```

If no arguments are provided, the script runs with default parameters.

### Tournament Results

The script outputs:
- Average payoff matrix showing scores for each player against each opponent.
- Total average scores, sorted from highest to lowest.
- List of winners based on total average scores.
- Detailed scores for each winner against other players.
- Maximum and minimum average individual gains between players.

## Strategies

1. **Angel**: Always cooperates.
2. **Diablo**: Always defects.
3. **Tito**: Mimics the opponent’s last move after cooperating in the first round.
4. **Loco**: Randomly cooperates or defects with equal probability.
5. **Resentido**: Cooperates unless the opponent has defected in the past.

## Customization

You can modify or add strategies by editing the `simulate_tournament` function and defining a new strategy in the `players` dictionary.

Example of a new strategy:
```python
def custom_strategy(round_num, my_history, opp_history):
    # Custom logic here
    return 'C'  # or 'D'
```
Add the new strategy to the `players` dictionary:
```python
players['Custom'] = custom_strategy
```