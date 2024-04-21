import random
from collections import Counter

# Constants
CHOICES = ["rock", "paper", "scissors"]
INDEX = {"rock": 0, "paper": 1, "scissors": 2}

# Initialize frequency distributions and transition tables
FREQ_DIST_WIN = {f"{x}{y}": 1 for x in CHOICES for y in CHOICES}
FREQ_DIST_LOSE = {f"{x}{y}": 1 for x in CHOICES for y in CHOICES}
FREQ_DIST_TIE = {f"{x}{y}": 1 for x in CHOICES for y in CHOICES}

TRANSITION_WIN = [[1 / 3] * 3 for _ in range(3)]
TRANSITION_LOSE = [[1 / 3] * 3 for _ in range(3)]
TRANSITION_TIE = [[1 / 3] * 3 for _ in range(3)]

# Function to update frequency distributions
def update_freq_dist(previous_choice, current_choice, previous_result):
    key = previous_choice + current_choice
    if previous_result == "WIN":
        FREQ_DIST_WIN[key] += 1
    elif previous_result == "LOSE":
        FREQ_DIST_LOSE[key] += 1
    else:
        FREQ_DIST_TIE[key] += 1

# Function to update transition tables
def update_transition_table(previous_result):
    if previous_result == "WIN":
        rock = sum(FREQ_DIST_WIN[f"rock{x}"] for x in CHOICES)
        paper = sum(FREQ_DIST_WIN[f"paper{x}"] for x in CHOICES)
        scissors = sum(FREQ_DIST_WIN[f"scissors{x}"] for x in CHOICES)
        for i in range(3):
            for j in range(3):
                current_freq = FREQ_DIST_WIN[CHOICES[i] + CHOICES[j]]
                if i == 0:
                    TRANSITION_WIN[i][j] = current_freq / rock
                elif i == 1:
                    TRANSITION_WIN[i][j] = current_freq / paper
                else:
                    TRANSITION_WIN[i][j] = current_freq / scissors
    elif previous_result == "LOSE":
        rock = sum(FREQ_DIST_LOSE[f"rock{x}"] for x in CHOICES)
        paper = sum(FREQ_DIST_LOSE[f"paper{x}"] for x in CHOICES)
        scissors = sum(FREQ_DIST_LOSE[f"scissors{x}"] for x in CHOICES)
        for i in range(3):
            for j in range(3):
                current_freq = FREQ_DIST_LOSE[CHOICES[i] + CHOICES[j]]
                if i == 0:
                    TRANSITION_LOSE[i][j] = current_freq / rock
                elif i == 1:
                    TRANSITION_LOSE[i][j] = current_freq / paper
                else:
                    TRANSITION_LOSE[i][j] = current_freq / scissors
    else:  # TIE
        rock = sum(FREQ_DIST_TIE[f"rock{x}"] for x in CHOICES)
        paper = sum(FREQ_DIST_TIE[f"paper{x}"] for x in CHOICES)
        scissors = sum(FREQ_DIST_TIE[f"scissors{x}"] for x in CHOICES)
        for i in range(3):
            for j in range(3):
                current_freq = FREQ_DIST_TIE[CHOICES[i] + CHOICES[j]]
                if i == 0:
                    TRANSITION_TIE[i][j] = current_freq / rock
                elif i == 1:
                    TRANSITION_TIE[i][j] = current_freq / paper
                else:
                    TRANSITION_TIE[i][j] is scissors

# Function to decide winner based on choices
def decide_winner(player_choice, ai_choice):
    if player_choice == ai_choice:
        return "TIE"
    elif (
        (player_choice == "rock" and ai_choice == "scissors") or
        (player_choice == "paper" and ai_choice == "rock") or
        (player_choice == "scissors" and ai_choice == "paper")
    ):
        return "WIN"
    else:
        return "LOSE"

# Define AI strategy
def ai_strategy(previous_choice, previous_result):
    if previous_result == "WIN":
        predicted_probabilities = TRANSITION_WIN[INDEX[previous_choice]]
    elif previous_result == "LOSE":
        predicted_probabilities = TRANSITION_LOSE[INDEX[previous_choice]]
    else:
        predicted_probabilities = TRANSITION_TIE[INDEX[previous_choice]]

    predicted_move = CHOICES[
        predicted_probabilities.index(max(predicted_probabilities))
    ]

    # AI plays to counter the predicted move
    if predicted_move == "rock":
        return "paper"
    elif predicted_move == "paper":
        return "scissors"
    else:
        return "rock"

# Testing different strategies against this AI
def test_strategy(strategy_function, rounds):
    scores = Counter({"WIN": 0, "LOSE": 0, "TIE": 0})
    player_moves = []
    ai_moves = []
    results = []

    for round_num in range(rounds):
        if round_num == 0:
            player_choice = strategy_function(round_num, player_moves, results)
            ai_choice = random.choice(CHOICES)
        else:
            previous_choice = player_moves[-1]
            previous_result = results[-1]
            player_choice = strategy_function(round_num, player_moves, results)
            ai_choice = ai_strategy(previous_choice, previous_result)

        # Decide the winner and update stats
        decision = decide_winner(player_choice, ai_choice)
        scores[decision] += 1
        player_moves.append(player_choice)
        ai_moves.append(ai_choice)
        results.append(decision)

        # Update frequency distributions and transition tables
        if round_num > 0:
            update_freq_dist(previous_choice, player_choice, previous_result)
            update_transition_table(previous_result)

    total_games = sum(scores.values())
    win_rate = scores["WIN"] / total_games * 100
    return win_rate, scores


# Strategy functions
def random_strategy(round_num, player_moves, results):
    return random.choice(CHOICES)

def loop_strategy(round_num, player_moves, results):
    return CHOICES[round_num % 3]

def win_stay_lose_change_strategy(round_num, player_moves, results):
    if round_num == 0:
        return random.choice(CHOICES)
    elif results[-1] == "WIN":
        return player_moves[-1]  # Stay with the winning move
    elif player_moves[-1] == "rock":
        return "paper"  # Change to the next move
    elif player_moves[-1] == "paper":
        return "scissors"
    else:
        return "rock"

# Majority strategy implementation
# Might be interesting but maybe not realistic
# Works well against our AI but wouldn't against a random bot
def majority_strategy(round_num, player_moves, results):
    if round_num == 0:
        return random.choice(CHOICES)  # Random for the first round
    else:
        # Count occurrences of each move
        move_count = Counter(player_moves)
        # Select the move with the highest count
        most_frequent = move_count.most_common(1)[0][0]
        # Return the next move in a way that counters the AI
        if most_frequent == "rock":
            return "paper"  # Paper beats rock
        elif most_frequent == "paper":
            return "scissors"  # Scissors beat paper
        else:
            return "rock"  # Rock beats scissors

# Test different strategies against the AI bot for 100 rounds each
num_rounds = 1000
random_win_rate, random_scores = test_strategy(random_strategy, num_rounds)
loop_win_rate, loop_scores = test_strategy(loop_strategy, num_rounds)
win_stay_lose_change_win_rate, win_stay_lose_change_scores = test_strategy(win_stay_lose_change_strategy, num_rounds)
majority_win_rate, majority_scores = test_strategy(majority_strategy, num_rounds)

print("Random Strategy Win Rate:", random_win_rate, "%")
print("Loop Strategy Win Rate:", loop_win_rate, "%")
print("Win-Stay-Lose-Change Strategy Win Rate:", win_stay_lose_change_win_rate, "%")
print("Majority Strategy Win Rate:", majority_win_rate, "%")
