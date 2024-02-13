
class Stack:
    def __init__(self):
        self.array = []

    def push(self, element):
         self.array.insert(0, element)

    def pop(self):
        if self.isEmpty():
            raise IndexError("Stack is empty. Pop operation failed.")
        else:
            return self.array.pop(0)

    def peek(self):
        return self.array[0]

    def isEmpty(self):
        size = len(self.array)
        if size == 0:
            return True
        else:
            return False

    def size(self):
        return len(self.array)

    def __repr__(self):
        return str(self.array)
