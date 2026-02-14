def process_data(d):
    x = 0
    for i in d:
        x += i
    return x

def average(d):
    x = process_data(d)
    return x / len(d)
