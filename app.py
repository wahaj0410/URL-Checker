import requests 
import time
from datetime import datetime

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