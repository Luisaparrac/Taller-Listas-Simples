from models.node import Node


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def insert_first(self, value):
        node = Node(value)
        node.next = self.head
        self.head = node
        if self.tail is None:
            self.tail = node
        self.length += 1
        return node

    def insert_last(self, value):
        node = Node(value)
        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.length += 1
        return node

    def insert_at(self, index, value):
        if index <= 0 or self.head is None:
            return self.insert_first(value)
        if index >= self.length:
            return self.insert_last(value)

        previous = self._node_before(index)
        node = Node(value)
        node.next = previous.next
        previous.next = node
        self.length += 1
        return node

    def remove_at(self, index):
        if self.head is None or index < 0 or index >= self.length:
            return None

        if index == 0:
            removed = self.head
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.length -= 1
            return removed.value

        previous = self._node_before(index)
        removed = previous.next
        previous.next = removed.next
        if removed is self.tail:
            self.tail = previous
        self.length -= 1
        return removed.value

    def get(self, index):
        node = self._node_at(index)
        return node.value if node else None

    def find_node(self, predicate):
        current = self.head
        while current is not None:
            if predicate(current.value):
                return current
            current = current.next
        return None

    def index_of(self, predicate):
        current = self.head
        index = 0
        while current is not None:
            if predicate(current.value):
                return index
            current = current.next
            index += 1
        return -1

    def move_node(self, node, target_index):
        if node is None:
            return

        previous = None
        current = self.head
        while current is not None and current is not node:
            previous = current
            current = current.next
        if current is None:
            return

        if previous is None:
            self.head = node.next
        else:
            previous.next = node.next
        if node is self.tail:
            self.tail = previous
        node.next = None
        self.length -= 1

        if target_index <= 0 or self.head is None:
            node.next = self.head
            self.head = node
            if self.tail is None:
                self.tail = node
        elif target_index >= self.length:
            if self.tail is not None:
                self.tail.next = node
            else:
                self.head = node
            self.tail = node
        else:
            insert_before = self._node_before(target_index)
            node.next = insert_before.next
            insert_before.next = node
        self.length += 1

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def size(self):
        return self.length

    def is_empty(self):
        return self.length == 0

    def _node_at(self, index):
        if index < 0 or index >= self.length:
            return None
        current = self.head
        for _ in range(index):
            current = current.next
        return current

    def _node_before(self, index):
        current = self.head
        for _ in range(index - 1):
            current = current.next
        return current
