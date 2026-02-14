def analyze_scores(scores):
    average = 0
    total = sum(scores)
    if len(scores) > 0:
        average = total / len(scores)
    return average

def print_summary(scores):
    avg = analyze_scores(scores)
    print(f"Scores: {scores}, Average: {avg}")
