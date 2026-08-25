import os
import tempfile
import unittest

from module import PersistentPriorityQueue


class TestPersistentPriorityQueue(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()

        self.queue = PersistentPriorityQueue(self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_insert(self):
        item = self.queue.insert("Task A", 5)

        self.assertEqual(item["value"], "Task A")
        self.assertEqual(item["priority"], 5)

    def test_extract_min(self):
        self.queue.insert("Low Priority", 5)
        self.queue.insert("High Priority", 1)

        result = self.queue.extract_min()

        self.assertEqual(result["value"], "High Priority")
        self.assertEqual(result["priority"], 1)

    def test_extract_max(self):
        self.queue.insert("Task A", 2)
        self.queue.insert("Task B", 8)

        result = self.queue.extract_max()

        self.assertEqual(result["value"], "Task B")
        self.assertEqual(result["priority"], 8)

    def test_peek(self):
        self.queue.insert("Task A", 5)
        self.queue.insert("Important Task", 1)

        result = self.queue.peek()

        self.assertEqual(result["value"], "Important Task")

        # Peek should NOT remove the item
        self.assertFalse(self.queue.is_empty())

    def test_update(self):
        item = self.queue.insert("Task A", 5)

        updated = self.queue.update(item["id"], 1)

        self.assertEqual(updated["priority"], 1)
        self.assertEqual(self.queue.peek()["priority"], 1)

    def test_delete(self):
        item = self.queue.insert("Task A", 5)

        deleted = self.queue.delete(item["id"])

        self.assertEqual(deleted["value"], "Task A")
        self.assertTrue(self.queue.is_empty())

    def test_is_empty(self):
        self.assertTrue(self.queue.is_empty())

        self.queue.insert("Task A", 5)

        self.assertFalse(self.queue.is_empty())

    def test_persistence(self):
        self.queue.insert("Persistent Task", 1)

        # Create a completely new queue using the same storage file
        new_queue = PersistentPriorityQueue(self.temp_file.name)

        result = new_queue.peek()

        self.assertEqual(result["value"], "Persistent Task")
        self.assertEqual(result["priority"], 1)

    def test_is_empty(self):
        self.assertTrue(self.queue.is_empty())

        self.queue.insert("Task A", 5)

        self.assertFalse(self.queue.is_empty())

    def test_persistence(self):
        self.queue.insert("Persistent Task", 1)

        new_queue = PersistentPriorityQueue(self.temp_file.name)

        result = new_queue.peek()

        self.assertEqual(result["value"], "Persistent Task")
        self.assertEqual(result["priority"], 1)

    def test_extract_from_empty_queue(self):
        self.assertIsNone(self.queue.extract_min())
        self.assertIsNone(self.queue.extract_max())

    def test_peek_empty_queue(self):
        self.assertIsNone(self.queue.peek())

    def test_update_nonexistent_item(self):
        result = self.queue.update(999, 10)

        self.assertIsNone(result)

    def test_delete_nonexistent_item(self):
        result = self.queue.delete(999)

        self.assertIsNone(result)
if __name__ == "__main__":
    unittest.main()