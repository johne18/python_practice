## Why does async exist

Synchronous processes are structured like this:  
- Synchronous: do A → wait → do B → wait → do C  

With async:
- Threads: A and B can make progress concurrently using separate threads  
- Async: A starts an I/O operation → while it waits, the event loop runs B → then resumes A when its I/O is ready



**IMPORTANT**  
Async doesn't make CPU-heavy python code faster, it makes programs more *efficient* when they're spending time waiting for I/O  



**Key difference between concurrency and async**  
Concurrency is a way of structuring work.  
"I have multiple things in progress at the same time"  
Async is a programming technique to implement concurrency efficiently.  
Suppose you need to call 3 APIs

```
API A: ──────────────── response
API B: ───────────── response
API C: ─────────────────── response
```

```
Synchronous:
Call A → wait → Call B → wait → Call C → wait

Asynchronous:
Call A ─────────────────┐
Call B ────────────────┐│
Call C ───────────────┐││
                      ↓↓↓
                   responses
```

While A is waiting for the network, python can work on B or C.  



## What is a coroutine?
- a piece of async work that can pause itself and later resume where it left off.
- the keyword async is what defines a coroutine function.
- awaits must happen inside an async context.


#### Coroutine function  
```
async def get_user():
    response = await fetch_user()
    return response

coro = get_user()
```
This way of writing doesn't actually run get_user() yet, but gives a coroutine object.  
If you do await coro, it basically is sayig run the coroutine now and wait for it to finish before your current coroutine continues.  
Defeats the purpose of async. You would instead create a task to schedule it.


#### Creating a task
```
task = asyncio.create_task(get_user())

print("I'm doing something else")

result = await task
```
Telling the event loop to schedule this coroutine run.


#### Key difference
```
user = await get_user()
orders = await get_orders()

get_user()
    ↓
WAIT
    ↓
result
    ↓
get_orders()
    ↓
WAIT
    ↓
result

Still sequential
```


```
user_task = asyncio.create_task(get_user())
orders_task = asyncio.create_task(get_orders())

user = await user_task
orders = await orders_task

get_user()   ────────────────┐
                             ├── concurrent
get_orders() ────────────────┘
```


#### Examples
Processing a customer.  
You need
- their orders
- account balance
- their preferences  

Imagine that information can be fetched through APIs. If all three can be called using the user_id and don't depend on each other's results, you can do this
```
user = await get_user(user_id)

orders_task = asyncio.create_task(get_orders(user_id))
balance_task = asyncio.create_task(get_balance(user_id))
prefs_task = asyncio.create_task(get_preferences(user_id))

orders = await orders_task
balance = await balance_task
prefs = await prefs_task
```
Now suppose you need the address, shipping_options and placing the order.  
You can't get the address until you know the user, can't get shipping options until you know the address, and can't place the order until you know the shipping option.
```
user = await get_user(user_id)

address = await get_address(user.address_id)

options = await get_shipping_options(address)

order = await place_order(options[0])
```






## What is an event loop?
- Like a traffic controller for asynchronous work.  
- Always asking what work is ready to run right now, and what work is pending?  
- Keeps track of all these operations and resumes them when they can make progress
- When a coroutine reaches an await, it tells the event loop:  
"I can't continue until this call has soething for me. Go run something else and come back later"
- It's not doing the work concurrently, it's coordinating it, like an orchestrator.





## What is meant by A waiting for the network?
Example
```
response = requests.get("https://api.example.com/users/123")

Your Python program
       |
       |  "Give me user 123"
       ↓
    Network
       |
       ↓
API server
       |
       |  processes request
       |  ███████████████
       ↓
    Network
       |
       ↓
Your Python program
```

There can be ms to seconds of wait time between sending the request and receiving the response. Python can't do anything b/c it needs the response.  
Meaning, the CPU isn't doing something usefule during that wait time.  

```
async def get_user(user_id):
    response = await fetch_user(user_id)
    return response
```
When the execution reaches await, the event loop is saying:  
"Okay, this operation is waiting for network I/O. I'll come back to it when the network response is ready."  

Conceptually
```
Time →

Task A:  SEND ───── WAIT ───────────── RESPONSE
Task B:       SEND ─────── WAIT ─────── RESPONSE
Task C:          SEND ────────── WAIT ───── RESPONSE

CPU:     A       B        C       A       B       C

There is one CPU thread here. We're not necessarily executing A, B, and C simultaneously.

We're interleaving them while they're waiting.

How it looks like step-by-step:
1. Python starts the network request
          ↓
2. OS/network stack takes over
          ↓
3. Coroutine says "I'm waiting"
          ↓
4. Event loop runs other work
          ↓
5. OS tells event loop:
       "Data for that network request is ready"
          ↓
6. Event loop resumes get_user()
          ↓
7. fetch_user() returns
```

First case
```
A → waiting for network
B → waiting for network
C → ready to run
.
.
.
A → network data ready!
B → waiting
C → waiting

OS notifies the event loop that A's network operation can proceed, and repeats for other await calls.
```

Second Case
```
A → network data ready!
B → waiting for network
C → ready to run

The event loop would look something like this.

        Event Loop
            │
      ┌─────┴─────┐
      ↓           ↓
   A is ready   C is ready
      │           │
      └─────┬─────┘
            ↓
       Pick one

General behavior, FIFO. Whichever one is ready first will continue.
```

So, await is where a coroutine gives the event loop an opportunity to run other work.














## Mental notes

### Coroutine
"Here's some async work I know how to do."
```
async def fetch():
    ...
```

### await  
"I'm waiting. Give someone else a turn."
```
await fetch()
```

### Event loop  
"I'll keep track of everyone who's waiting and run whoever is ready."
```
             EVENT LOOP
                  │
       ┌──────────┼──────────┐
       ↓          ↓          ↓
      A           B          C
    waiting     ready      waiting
                  │
                  ↓
               RUN B
                  │
               await
                  │
                  ↓
             check again
```

### create_task  
"Event loop, schedule this coroutine to run"
```
task1 = asyncio.create_task(call_api(1))
task2 = asyncio.create_task(call_api(2))

# Both have been scheduled.
# Do other work...

result1 = await task1
result2 = await task2
```

### gather  
"Run these operations concurrently and give me their results once they're all done"
```
# More useful for batch processing
results = await asyncio.gather(
    call_api(1),
    call_api(2),
    call_api(3),
)
```

### Semaphore  
"I'll limit the number of coroutines that can enter. Controls concurrency, but doesn't control the number of requests that can be sent per second"  
```
# Limit the number of coroutines to 20
semaphore = asyncio.Semaphore(20)
```

### Rate Limiting
"How frequent should I send requests to a service?"
```
# Configure for a max of 50 requests every 10 seconds.
from aiolimiter import AsyncLimiter
limiter = AsyncLimiter(max_rate=50, time_period=10)
```

### asyncio.Queue
"How much can we hold for later?"

### Python async vs architectural async
Efficiency w/in an application  
The client doesn't need to wait for the work to finish



## Difference between yield and await
## What is rate limiting
## What is a asyncio.Queue




## Use cases
- REST APIs
- Database queries
- Reading/writing over a network
- Web scraping
- Message queues