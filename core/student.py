from core.person import Person
from typing import List

class Student(Person):
    """Inheritance from Person + Polymorphism"""

    def __init__(self, student_id: str, name: str):
        super().__init__(student_id, name)
        self._borrowed_transactions: List["Transaction"] = []  

    def get_role(self) -> str:
        return "Student"

    def add_transaction(self, transaction: "Transaction"):
        self._borrowed_transactions.append(transaction)

    def has_overdue(self) -> bool:
        return any(t.is_overdue() for t in self._borrowed_transactions if not t.is_returned())

    # Polymorphism: Override parent method
    def display_info(self) -> str:
        base = super().display_info()
        overdue = "Yes" if self.has_overdue() else "No"
        return f"{base} | Borrowed: {len(self._borrowed_transactions)} | Has Overdue: {overdue}"
