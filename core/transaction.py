from datetime import datetime

class Transaction:
    def __init__(self, student, book, due_date):
        self.student = student
        self.book = book
        self.borrow_date = datetime.now()
        self.due_date = due_date
        self._returned = False

    def is_returned(self):
        return self._returned

    def mark_as_returned(self):
        self._returned = True
