from module import PersistentPriorityQueue

queue = PersistentPriorityQueue()

# Insert items
queue.insert("Database Down", 1)
queue.insert("Fix Login Bug", 3)
queue.insert("New Feature", 8)

print("Peek:", queue.peek())

print("Extract Min:", queue.extract_min())

print("Extract Max:", queue.extract_max())

print("Is Empty:", queue.is_empty())