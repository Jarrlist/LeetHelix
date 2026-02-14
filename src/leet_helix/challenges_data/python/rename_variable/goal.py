def process_data(data):
    total = 0
    for i in data:
        total += i
    return total

def average(data):
    total = process_data(data)
    return total / len(data)
