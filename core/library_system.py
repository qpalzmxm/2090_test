from core.student import Student
from core.book import Book
from core.transaction import Transaction
from core.librarian import Librarian
from typing import Dict, Optional

class LibrarySystem:
    """Main class using Composition"""

    def __init__(self):
        self._students: Dict[str, Student] = {}
        self._books: Dict[str, Book] = {}           # key = barcode
        self._transactions = []
        self._librarian = Librarian("LIB001", "Admin")

    def add_student(self, student_id: str, name: str) -> bool:
        if student_id in self._students:
            print("Student ID already exists!")
            return False
        self._students[student_id] = Student(student_id, name)
        print(f"Student {name} added successfully.")
        return True

    def add_book(self, isbn: str, title: str, barcode: str, quantity: int = 1) -> bool:
        if barcode in self._books:
            print("Barcode already exists!")
            return False
        self._books[barcode] = Book(isbn, title, barcode, quantity)
        print(f"Book '{title}' added with barcode {barcode}.")
        return True

    def borrow_book(self, student_id: str, barcode: str, days: int = 14) -> bool:
        student = self._students.get(student_id)
        book = self._books.get(barcode)

        if not student:
            print("Student not found!")
            return False
        if not book:
            print("Book not found!")
            return False
        if student.has_overdue():
            print("Cannot borrow: Student has overdue book(s)!")
            return False
        if not book.borrow_one():
            print("Book not available!")
            return False

        transaction = Transaction(student, book, days)
        student.add_transaction(transaction)
        self._transactions.append(transaction)
        print(f"Book borrowed successfully! Due date: {transaction.due_date.date()}")
        return True

    def return_book(self, barcode: str, fee_paid: float = 0.0):
        for t in self._transactions:
            if t.book.barcode == barcode and not t.is_returned():
                t.mark_returned(fee_paid)
                t.book.return_one()
                print(f"Book returned. Fee paid: HKD {fee_paid:.2f}")
                if t.is_overdue():
                    print(f"Note: Overdue fee was HKD {t.calculate_fee():.2f}")
                return
        print("No active borrow record found for this barcode!")

    def search_book(self, barcode: str) -> Optional[Book]:
        return self._books.get(barcode)

    def show_all_students(self):
        print("\n=== All Students ===")
        for student in self._students.values():
            print(student.display_info())

    def show_all_books(self):
        print("\n=== All Books ===")
        for book in self._books.values():
            print(book.display_info())
