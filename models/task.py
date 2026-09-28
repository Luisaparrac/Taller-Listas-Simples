class Task:
    _next_id = 1

    def __init__(self, title, priority):
        self.id = Task._next_id
        Task._next_id += 1
        self.title = title
        self.priority = priority
        self.done = False

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "done": self.done,
        }
