def fetch_data(url, method, retries, cache, timeout):
    print(f"Fetching {url}...")

def main():
    # Call 1: Simple values
    fetch_data("api/v1", "GET", 3, True, 30)

    # Call 2: Complex values (gw would be slow here)
    fetch_data("api/v2", "POST", 5, False, 6000)

    # Call 3: Mixed types
    fetch_data("api/v3", "PUT", 1, None, float('inf'))
