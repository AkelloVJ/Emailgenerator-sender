import threading
import queue
import requests
import sys

NUM_THREADS = 10
API_ENDPOINT = "http://ipinfo.io/json"
TIMEOUT = 5

q = queue.Queue()
valid_proxies = []
output_lock = threading.Lock()

with open("proxylistunclean.txt", "r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)

def check_proxies():
    global q, valid_proxies
    while not q.empty():
        proxy = q.get()
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
            res = requests.get(API_ENDPOINT, proxies={"http": proxy, "https": proxy}, headers=headers, timeout=TIMEOUT)
        except requests.RequestException as e:
            print(f"Error checking proxy {proxy}: {e}")
            continue
        if res.status_code == 200:
            with output_lock:
                print(proxy)
                sys.stdout.flush()  # Flush the output to ensure immediate display
                valid_proxies.append(proxy)

# Create and start threads
threads = []
for _ in range(NUM_THREADS):
    thread = threading.Thread(target=check_proxies)
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Save valid proxies to a file
with open("proxylist.txt", "w") as output_file:
    for proxy in valid_proxies:
        output_file.write(f"{proxy}\n")

print("Valid proxies saved to proxylist.txt")
