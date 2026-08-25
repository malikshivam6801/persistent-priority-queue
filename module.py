import json
import heapq
import os


class PersistentPriorityQueue:
    """
    Persistent Priority Queue using binary heaps.

    The queue maintains:
    - A min-heap for extract_min()
    - A max-heap for extract_max()
    - A dictionary for the current active items

    Data is persisted to a JSON file.
    """

    def __init__(self, storage_file="priority_queue.json"):
        self.storage_file = storage_file

        # Min heap: (priority, item_id)
        self.min_heap = []

        # Max heap: (-priority, item_id)
        self.max_heap = []

        # Active items: item_id -> item
        self.items = {}

        self.next_id = 1

        self._load()

    # ---------------------------------------------------------
    # Persistence
    # ---------------------------------------------------------

    def _save(self):
        """Save the current queue state to JSON."""
        data = {
            "next_id": self.next_id,
            "items": list(self.items.values())
        }

        temp_file = self.storage_file + ".tmp"

        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        os.replace(temp_file, self.storage_file)

    def _load(self):
        """Load queue state from JSON and rebuild the heaps."""
        if not os.path.exists(self.storage_file):
            return

        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.next_id = data.get("next_id", 1)

            for item in data.get("items", []):
                item_id = item["id"]

                self.items[item_id] = item

                heapq.heappush(
                    self.min_heap,
                    (item["priority"], item_id)
                )

                heapq.heappush(
                    self.max_heap,
                    (-item["priority"], item_id)
                )

        except (json.JSONDecodeError, OSError, KeyError, TypeError):
            self.next_id = 1
            self.min_heap = []
            self.max_heap = []
            self.items = {}

    # ---------------------------------------------------------
    # Helper methods
    # ---------------------------------------------------------

    def _get_min_item(self):
        """Return the current minimum item without removing it."""
        while self.min_heap:
            priority, item_id = self.min_heap[0]

            item = self.items.get(item_id)

            if item is not None and item["priority"] == priority:
                return item

            # Remove stale heap entry
            heapq.heappop(self.min_heap)

        return None

    def _get_max_item(self):
        """Return the current maximum item without removing it."""
        while self.max_heap:
            negative_priority, item_id = self.max_heap[0]

            priority = -negative_priority
            item = self.items.get(item_id)

            if item is not None and item["priority"] == priority:
                return item

            # Remove stale heap entry
            heapq.heappop(self.max_heap)

        return None

    # ---------------------------------------------------------
    # Required Priority Queue Operations
    # ---------------------------------------------------------

    def insert(self, value, priority):
        """Insert a new item into the priority queue."""

        if not isinstance(priority, (int, float)):
            raise TypeError("Priority must be a number.")

        item = {
            "id": self.next_id,
            "value": value,
            "priority": priority
        }

        self.items[self.next_id] = item

        heapq.heappush(
            self.min_heap,
            (priority, self.next_id)
        )

        heapq.heappush(
            self.max_heap,
            (-priority, self.next_id)
        )

        self.next_id += 1

        self._save()

        return item

    def extract_min(self):
        """Remove and return the item with the smallest priority."""

        item = self._get_min_item()

        if item is None:
            return None

        item_id = item["id"]

        del self.items[item_id]

        heapq.heappop(self.min_heap)

        self._save()

        return item

    def extract_max(self):
        """Remove and return the item with the largest priority."""

        item = self._get_max_item()

        if item is None:
            return None

        item_id = item["id"]

        del self.items[item_id]

        heapq.heappop(self.max_heap)

        self._save()

        return item

    def peek(self):
        """Return the minimum-priority item without removing it."""

        return self._get_min_item()

    def update(self, item_id, new_priority):
        """Update the priority of an existing item."""

        if not isinstance(new_priority, (int, float)):
            raise TypeError("Priority must be a number.")

        item = self.items.get(item_id)

        if item is None:
            return None

        item["priority"] = new_priority

        # Add new heap entries.
        # Old entries become stale and are ignored automatically.
        heapq.heappush(
            self.min_heap,
            (new_priority, item_id)
        )

        heapq.heappush(
            self.max_heap,
            (-new_priority, item_id)
        )

        self._save()

        return item

    def delete(self, item_id):
        """Delete an item using its ID."""

        item = self.items.pop(item_id, None)

        if item is None:
            return None

        self._save()

        return item

    def is_empty(self):
        """Return True if the priority queue is empty."""

        return len(self.items) == 0