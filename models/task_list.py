from models.linked_list import SinglyLinkedList
from models.task import Task


class TaskList:
    def __init__(self):
        self.tasks = SinglyLinkedList()
        self._seed()

    def _seed(self):
        self.tasks.insert_last(Task("Sketch the wireframes", "high"))
        self.tasks.insert_last(Task("Review pull request", "medium"))
        self.tasks.insert_last(Task("Water the office plants", "low"))
        self.tasks.insert_last(Task("Write the weekly report", "medium"))

    def add_task(self, title, priority, position=None):
        task = Task(title, priority)
        if position is None:
            self.tasks.insert_last(task)
        else:
            self.tasks.insert_at(position, task)
        return task

    def toggle_task(self, task_id):
        node = self.tasks.find_node(lambda t: t.id == task_id)
        if node is not None:
            node.value.done = not node.value.done
        return node

    def remove_task(self, task_id):
        index = self.tasks.index_of(lambda t: t.id == task_id)
        if index == -1:
            return None
        return self.tasks.remove_at(index)

    def move_task_to(self, task_id, target_index):
        node = self.tasks.find_node(lambda t: t.id == task_id)
        if node is None:
            return
        self.tasks.move_node(node, target_index)

    def clear_completed(self):
        node = self.tasks.find_node(lambda t: t.done)
        while node is not None:
            self.remove_task(node.value.id)
            node = self.tasks.find_node(lambda t: t.done)

    def traversal_order(self):
        order = []
        current = self.tasks.head
        while current is not None:
            order.append(current.value.id)
            current = current.next
        return order

    def state(self):
        payload = []
        done_count = 0
        current = self.tasks.head
        while current is not None:
            payload.append(current.value.to_dict())
            if current.value.done:
                done_count += 1
            current = current.next

        return {
            "tasks": payload,
            "size": self.tasks.size(),
            "done_count": done_count,
        }
