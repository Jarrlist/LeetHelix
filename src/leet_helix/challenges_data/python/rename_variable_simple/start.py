def analyze_scores(user_score_history):
    calculated_average_value = 0
    total = sum(user_score_history)
    if len(user_score_history) > 0:
        calculated_average_value = total / len(user_score_history)
    return calculated_average_value

def print_summary(user_score_history):
    avg = analyze_scores(user_score_history)
    print(f"Scores: {user_score_history}, Average: {avg}")
