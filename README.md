# URL-Checker

## How it works

### Imports and setup
- `requests` — lets Python make HTTP calls to check if a website responds
- `time` — measures how long each request takes, and pauses between checks
- `datetime` — generates readable timestamps for logs and console output
- `sys` — lets the program exit cleanly when stopped
- `HEADERS` — a custom User-Agent so sites like Wikipedia don't block the request as a bot
- `websites` — the list of URLs being monitored

### check_website(url)
Sends a request to a single URL with a 5-second timeout, so it doesn't hang forever on a slow or unresponsive site. Measures how long the response takes, then returns a dictionary describing the result — whether it's up, the status code, the response time, or an error.

Wrapped in try/except so a single dead site can't crash the whole program. If the connection fails entirely (timeout, DNS failure, refused connection), that's caught and reported as "down" instead of throwing an unhandled error.

### print_result(result)
Takes that result dictionary and prints one clean, readable line: a timestamp, UP/DOWN status, the URL, and either the response time or the error message.

### log_result(result)
Same idea, but writes to a file instead of the console — so there's a permanent record of every check over time. Opens the file in "append" mode so old entries are preserved instead of erased on every run.

### check_all_sites()
Loops through the full list of websites, checking, printing, and logging each one. This represents one complete monitoring pass.

### main()
Wraps check_all_sites() in an infinite loop so it repeats automatically every 30 seconds instead of running once and exiting. Uses time.sleep() to pause between checks, and catches Ctrl+C (KeyboardInterrupt) so the program shuts down cleanly with a message instead of printing a scary error when stopped.

    import requests 
    import time
    from datetime import datetime
    import sys

    LOG_FILE = "status_log.txt"
    
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (status-checker learning project)"
    }
    
    websites = [
        "https://www.google.com",
        "https://www.github.com",
        "https://www.stackoverflow.com",
        "https://www.reddit.com",
        "https://www.wikipedia.org",
        "https://www.netflix.com"
    ]
    
    def check_website(url):
        try:
            start_time = time.time()
            response = requests.get(url, timeout=5, headers=HEADERS)
            elapsed_ms = round((time.time() - start_time) * 1000)
            return {
                "url": url,
                "status_code": response.status_code,
                "is_up": response.status_code == 200,
                "response_time_ms": elapsed_ms,
                "error": None
            }

    except requests.exceptions.RequestException as e:
        return {
            "url": url,
            "status_code": None,
            "is_up": False,
            "response_time_ms": None,
            "error": str(e)
        }
    
    def print_result(result):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if result["is_up"]:
            print(f"[{timestamp}] UP   {result['url']} - {result['status_code']} ({result['response_time_ms']}ms)")
        else:
            print(f"[{timestamp}] DOWN {result['url']} - {result['error'] or result['status_code']}")  
    
    
    def log_result(result):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            if result["is_up"]:
                f.write(f"{timestamp} | UP   | {result['url']} | {result['status_code']} | {result['response_time_ms']}ms\n")
            else:
                f.write(f"{timestamp} | DOWN | {result['url']} | {result['error'] or result['status_code']}\n")
    
    def check_all_sites():
        print(f"\n--- Checking {len(websites)} sites ---")
        for url in websites:
            result = check_website(url)
            print_result(result)
            log_result(result)
    
    if __name__ == "__main__":
        check_all_sites()
    
    def main():
        interval = 30
        try:
            while True:
                check_all_sites()
                print(f"Waiting {interval} seconds before next check...\n(Press Ctrl+C to stop)")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nExiting status checker. Goodbye!")
            sys.exit(0)

    if __name__ == "__main__":
        main()  
