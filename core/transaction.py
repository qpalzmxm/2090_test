from datetime import datetime, timedelta

class Transaction:
    """Handles borrow/return logic"""

    def __init__(self, student, book, days: int = 14):
        self.student = student
        self.book = book
        self.borrow_date = datetime.now()
        self.due_date = self.borrow_date + timedelta(days=days)
        self.return_date = None
        self.fee_paid = 0.0
        self._status = "borrowed"

    def is_overdue(self) -> bool:
        if self.return_date:
            return False
        return datetime.now() > self.due_date

    def is_returned(self) -> bool:
        return self.return_date is not None

    def calculate_fee(self, daily_fee: float = 5.0) -> float:
        """Polymorphism-ready"""
        if not self.is_overdue() or self.return_date:
            return 0.0
        days_over = (datetime.now() - self.due_date).days
        return round(days_over * daily_fee, 2)

    def mark_returned(self, fee_paid: float):
        self.return_date = datetime.now()
        self.fee_paid = fee_paid
        self._status = "returned" if fee_paid >= self.calculate_fee() else "overdue"
