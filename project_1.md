### Project 1 — Concurrent API client

Imagine you have 10,000 IDs and need to retrieve data from an API. Fetch pokemon IDs from   
https://pokeapi.co/

Synchronous:
```
ID 1 → wait
ID 2 → wait
ID 3 → wait
...
```

Async:
```
ID 1 ────────┐
ID 2 ────────┤
ID 3 ────────┼──> responses arrive
ID 4 ────────┤
ID 5 ────────┘
```

Implement:
- concurrency limits
- timeouts
- retries
- exception handling
- cancellation
- result aggregation by type