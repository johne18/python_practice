## ThreadPoolExecutor

### Pros
- Simplest way to run existing sync code parallely w/ minimal change
- Automatically manages thread, creation, scheudling and cleanup
- Good for IO bound tasks
- Granular exception handling  
### Cons
- Not good for CPU-bound tasks
- Thread creation and context switching has overhead
- In-memory ishared state vars are thread un-safe  


```
# ====================
# Running without return value
# ====================
from concurrent.futures import ThreadPoolExecutor
import time

def log_message(message):
    # do stuff
    print(f"Logging: {message}")

def send_notification(user):
    # do other stuff
    print(f"Notifying: {user}")

def run():
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(log_message, "System started")
        executor.submit(send_notification, "Alice")
    # the context waits for all the submitted tasks to finish
    print("All tasks done")



# ====================
# Running w/ multiple inputs
# ====================
def process_url(url):
    # do stuff
    print(f"Processed: {url}")
    return f"Result for {url}"

def run():
    urls = ["http://cafecito.tech", "http://medium.com", "http://stuff.com"]
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(process_url, urls))
    print("All URLs processed", results)



# ====================
# Passing return values
# ====================
def fetch_data():    
    return "Data"

def process_data(data):
    # do stuff
    print(f"Processed data: {data}")

def run():
    with ThreadPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(fetch_data)
        # Wait for result and feed it to the second function
        res = future1.result()
        executor.submit(process_data, res)

    print("Pipeline completed")

```


