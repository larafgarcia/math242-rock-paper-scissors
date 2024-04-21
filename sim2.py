import random

# Define the possible moves
moves = ["rock", "paper", "scissors"]


# Function to determine the winner
def determine_winner(player_move, bot_move):
    if player_move == bot_move:
        return "tie"
    elif (player_move == "rock" and bot_move == "scissors") or \
            (player_move == "paper" and bot_move == "rock") or \
            (player_move == "scissors" and bot_move == "paper"):
        return "win"
    else:
        return "loss"


# Define strategies
def strategy_rock():
    return "rock"


def strategy_paper():
    return "paper"


def strategy_scissors():
    return "scissors"


def strategy_random():
    return random.choice(moves)


# Define the Win-Stay-Lose-Change strategy
class WinStayLoseChangeStrategy:
    def __init__(self):
        self.current_move = random.choice(moves)  # Start with a random move
        self.last_result = None  # No result initially

    def __call__(self):
        if self.last_result == "loss":
            self.current_move = random.choice(
                [m for m in moves if m != self.current_move]
            )
        return self.current_move

    def update_result(self, result):
        self.last_result = result


# Define the cyclic strategy (rock->paper->scissors)
class CyclicStrategy:
    def __init__(self):
        self.index = 0  # Start at the beginning of the moves list

    def __call__(self):
        current_move = moves[self.index % 3]  # Cycle through the moves
        self.index += 1  # Move to the next index
        return current_move


# Simulation function
def simulate(strategy, num_rounds=10000000000):
    wins = 0
    losses = 0
    ties = 0

    for _ in range(num_rounds):
        bot_move = random.choice(moves)
        player_move = strategy()
        result = determine_winner(player_move, bot_move)

        if hasattr(strategy, "update_result"):
            strategy.update_result(result)

        if result == "win":
            wins += 1
        elif result == "loss":
            losses += 1
        else:
            ties += 1

    win_percentage = (wins / num_rounds) * 100
    tie_percentage = (ties / num_rounds) * 100
    return win_percentage, tie_percentage


# Dictionary of strategies, including the cyclic strategy
strategies = {
    "Always Rock": strategy_rock,
    "Always Paper": strategy_paper,
    "Always Scissors": strategy_scissors,
    "Random Strategy": strategy_random,
    "Win-Stay-Lose-Change": WinStayLoseChangeStrategy(),
    "Cyclic Strategy": CyclicStrategy(),
}

# Run simulations for all strategies
results = {}

for name, strategy in strategies.items():
    if isinstance(strategy, WinStayLoseChangeStrategy) or isinstance(strategy, CyclicStrategy):
        win_percentage, tie_percentage = simulate(strategy, num_rounds=1000)
    else:
        win_percentage, tie_percentage = simulate(lambda: strategy(), num_rounds=1000)

    results[name] = {
        "win_percentage": win_percentage,
        "tie_percentage": tie_percentage
    }

# Display the results
for strategy, result in results.items():
    print(f"{strategy}: {result['win_percentage']:.2f}% win, {result['tie_percentage']:.2f}% ties")
