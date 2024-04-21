import random

# Define the possible moves
moves = ["rock", "paper", "scissors"]


# Define the function to determine the winner
def determine_winner(player_move, bot_move):
    # If the moves are the same, it's a tie
    if player_move == bot_move:
        return "tie"
    # Define win conditions
    elif (player_move == "rock" and bot_move == "scissors") or \
            (player_move == "paper" and bot_move == "rock") or \
            (player_move == "scissors" and bot_move == "paper"):
        return "win"
    # Otherwise, the bot wins
    else:
        return "loss"

# Win-Stay-Lose-Change strategy
class WinStayLoseChangeStrategy:
    def __init__(self):
        self.current_move = random.choice(moves)  # Start with a random move
        self.last_result = "tie"  # Initialize to avoid errors

    def __call__(self):
        if self.last_result == "loss":
            # If lost, change to a different move
            new_move = random.choice([m for m in moves if m != self.current_move])
            self.current_move = new_move
        # If win or tie, stay with the same move
        return self.current_move

    def update_result(self, result):
        self.last_result = result

# Define strategies
def strategy_rock():
    return "rock"


def strategy_paper():
    return "paper"


def strategy_scissors():
    return "scissors"

def strategy_random():
    return random.choice(moves)


# Dictionary to hold strategies
strategies = {
    "Always Rock": strategy_rock,
    "Always Paper": strategy_paper,
    "Always Scissors": strategy_scissors,
    "Random Strategy": strategy_random
}


# Define the simulation function
def simulate(strategy, num_rounds=1000):
    wins = 0
    losses = 0
    ties = 0

    for _ in range(num_rounds):
        bot_move = random.choice(moves)
        player_move = strategy()
        result = determine_winner(player_move, bot_move)

        strategy.update_result(result)

        if result == "win":
            wins += 1
        elif result == "loss":
            losses += 1
        else:
            ties += 1

    win_percentage = (wins / num_rounds) * 100
    return win_percentage, (ties / num_rounds) * 100

# Run simulations for multiple strategies
strategies = {
    "Always Rock": strategy_rock,
    "Always Paper": strategy_paper,
    "Always Scissors": strategy_scissors,
    "Random Strategy": strategy_random,
    "Win-Stay-Lose-Change": WinStayLoseChangeStrategy(),
}

results = {}


# Run simulations for all strategies

for name, strategy in strategies.items():
    if isinstance(strategy, WinStayLoseChangeStrategy):
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
