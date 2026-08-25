# Persistent Priority Queue

A persistent priority queue implementation in Python using binary heaps and JSON-based file storage.

## Overview

This project implements a priority queue whose state is persisted to a JSON file.

The queue supports the following operations:

- `insert`
- `extract_min`
- `extract_max`
- `peek`
- `update`
- `delete`
- `is_empty`

The implementation uses binary heaps to efficiently retrieve both minimum- and maximum-priority elements.

## Features

- Binary heap based priority queue
- Min-heap for `extract_min()`
- Max-heap for `extract_max()`
- JSON file-based persistence
- Automatic state loading when the queue starts
- Automatic state saving after modifications
- Unique item IDs
- Support for priority updates
- Handling of empty queues and invalid item IDs
- Automated unit tests

## Implementation

The main implementation is located in:

    module.py

The `PersistentPriorityQueue` class maintains:

1. A min-heap for retrieving the item with the smallest priority.
2. A max-heap for retrieving the item with the largest priority.
3. A dictionary containing the currently active items.
4. A JSON file for persistent storage.

## Priority Convention

A smaller priority number represents a higher priority.

Example:

    Priority 1 = Highest priority
    Priority 2
    Priority 3
    Priority 5 = Lower priority

Therefore:

- `extract_min()` returns the item with the smallest priority number.
- `extract_max()` returns the item with the largest priority number.

## Persistence

The queue state is stored in:

    priority_queue.json

Whenever the queue is modified, its current state is written to the JSON file.

When a new `PersistentPriorityQueue` instance is created, the stored data is loaded and the heaps are reconstructed.

This allows the queue to retain its state even after the Python process is closed and started again.

## Supported Operations

### insert(value, priority)

Adds a new item to the queue.

Example:

    queue.insert("Database Down", 1)

### extract_min()

Removes and returns the item with the smallest priority.

Example:

    queue.extract_min()

### extract_max()

Removes and returns the item with the largest priority.

Example:

    queue.extract_max()

### peek()

Returns the minimum-priority item without removing it.

Example:

    queue.peek()

### update(item_id, new_priority)

Updates the priority of an existing item.

Example:

    queue.update(1, 2)

### delete(item_id)

Removes an item using its ID.

Example:

    queue.delete(1)

### is_empty()

Checks whether the queue contains any active items.

Example:

    queue.is_empty()

## Time Complexity

| Operation | Complexity |
|---|---:|
| insert | O(log n) |
| extract_min | O(log n) |
| extract_max | O(log n) |
| peek | O(1) |
| update | O(log n) |
| delete | O(1) average |
| is_empty | O(1) |

The implementation uses lazy deletion for stale heap entries created by updates and deletions.

## Running the Project

Make sure Python is installed.

From the project directory, run:

    python

Then:

    from module import PersistentPriorityQueue

    queue = PersistentPriorityQueue()

    queue.insert("Database Down", 1)
    queue.insert("Fix Login Bug", 3)
    queue.insert("New Feature", 8)

    print(queue.peek())
    print(queue.extract_min())
    print(queue.extract_max())

The queue state will be persisted automatically in:

    priority_queue.json

## Running Tests

Automated tests are provided in:

    test_module.py

Run all tests using:

    python -m unittest

The tests cover:

- Insert
- Extract minimum
- Extract maximum
- Peek
- Update
- Delete
- Empty queue behavior
- Invalid item IDs
- Persistence

## Real-World Use Cases

### 1. Hospital Emergency Systems

Patients can be assigned priorities based on the severity of their condition. Critical cases can be processed before less urgent cases.

### 2. Operating Systems

Processes can be scheduled according to their priority so that important processes receive CPU time earlier.

### 3. Customer Support Systems

Support tickets can be prioritized based on severity.

Example:

    Payment failure = Priority 1
    Login problem = Priority 2
    General question = Priority 5

### 4. Network Systems

Network packets or tasks can be prioritized so that important traffic can be processed before lower-priority traffic.

### 5. Task Scheduling

Applications can use priority queues to determine which background job should be processed next.

## Project Structure

    persistent-priority-queue/
    |
    +-- module.py
    +-- test_module.py
    +-- README.md
    +-- priority_queue.json

`priority_queue.json` is generated automatically when the queue stores persistent data.

## Design Choice

A binary heap was selected because it provides efficient insertion and removal of priority elements.

Two heaps are maintained:

- Min-heap for minimum-priority retrieval
- Max-heap for maximum-priority retrieval

A dictionary is used to maintain the current active items and support efficient lookup by item ID.

JSON file storage was selected because the assignment permits file-based persistence and it keeps the project simple, portable, and easy to run without requiring an external database setup.

## Testing

The implementation was tested using Python's built-in `unittest` framework.

All automated tests pass successfully.

    Ran 12 tests
    OK

## Requirements

- Python 3.x
- No external Python packages are required.

## Author

SDE Assignment - Aug 2026