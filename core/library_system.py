from datetime import datetime, timedelta
import math

class LibrarySystem:
    def __init__(self):
        self._students = {}
        self._books = {}
        self._transactions = []
        self._password = "admin123"
        self._book_counter = 1
        self._daily_fee = 5.0
        self._borrow_days = 14
        self._email_logs = []
        self._default_categories = [
            f"{i+1}.{cat}" for i, cat in enumerate([
                "Fiction", "Science", "History", "Math", "Tech", "Art", "Music", 
                "Philosophy", "Health", "Travel", "Biography", "Business", "Kids", 
                "Sports", "Poetry", "Social", "Language", "Law", "Religion", "Reference"
            ])
        ]

    def login(self, password):
        return password == self._password

    def change_password(self, old_pwd, new_pwd):
        if old_pwd == self._password:
            self._password = new_pwd
            return True
        return False

    def add_student(self, sid, name):
        email = f"s{sid[:7]}@live.hkmu.edu.hk"
        from core.student import Student
        s = Student(sid, name)
        s.email = email
        self._students[sid] = s
        print(f"✅ Registered: {name} ({email})")

    def add_book(self, isbn, title, cat, qty):
        barcode = f"b{self._book_counter:06d}"
        from core.book import Book
        self._books[barcode] = Book(isbn, title, barcode, cat, qty)
        self._book_counter += 1
        print(f"✅ Added: {title} ({barcode})")

    def borrow_book(self, sid, bid):
        s, b = self._students.get(sid), self._books.get(bid)
        if s and b and b.available_quantity > 0:
            b.available_quantity -= 1
            b.borrow_count += 1
            due = datetime.now() + timedelta(days=self._borrow_days)
            from core.transaction import Transaction
            self._transactions.append(Transaction(s, b, due))
            print(f"✅ Borrowed: {b.title} | Due: {due.date()}")
        else: print("❌ Check ID or Stock.")

    def return_book(self, sid, bid):
        for t in self._transactions:
            if t.student.person_id == sid and t.book.barcode == bid and not t.is_returned():
                t.mark_as_returned()
                t.book.available_quantity += 1
                print(f"✅ Returned: {t.book.title}")
                return
        print("❌ Record not found.")

    def get_student_report(self, sid):
        s = self._students.get(sid)
        if not s: return None
        cur, overdue, fee, today, total_his = [], [], 0.0, datetime.now(), 0
        for t in self._transactions:
            if t.student.person_id == sid:
                total_his += 1
                if not t.is_returned():
                    diff = (t.due_date - today).days
                    if diff >= 0:
                        cur.append(f"{t.book.title} ({diff}d left)")
                    else:
                        overdue.append(f"{t.book.title} (OVERDUE {abs(diff)}d)")
                        fee += abs(diff) * self._daily_fee
        return {"name": s.name, "sid": s.person_id, "current": cur, "overdue": overdue, "fee": fee, "total": total_his}

    def get_top10_books(self):
        if not self._books:
            return []
        return sorted(self._books.values(), key=lambda x: x.borrow_count, reverse=True)[:10]

    def get_top10_cats(self):
        cat_map = {}
        lookup = {c.split('.')[0]: c.split('.')[1] for c in self._default_categories}
        for b in self._books.values():
            for idx in [i.strip() for i in b.categories.split(",")]:
                name = lookup.get(idx, idx)
                cat_map[name] = cat_map.get(name, 0) + b.borrow_count
        return sorted(cat_map.items(), key=lambda x: x[1], reverse=True)[:10]

    def get_paginated_books(self, page):
        all_b = list(self._books.values())
        total_p = math.ceil(len(all_b) / 10) if all_b else 1
        return all_b[(page-1)*10 : page*10], total_p, len(all_b)

    def _auto_scan_emails(self):
        today = datetime.now()
        self._email_logs = []
        for t in self._transactions:
            if t.is_returned(): continue
            diff = (t.due_date - today).days
            email = getattr(t.student, 'email', "N/A")
            if 0 <= diff <= 3:
                self._email_logs.append(f"[REMINDER] To: {email} | {diff} days left | Book: {t.book.title}")
            elif diff < 0:
                days_overdue = abs(diff)
                if days_overdue % 7 == 0:
                    fee = days_overdue * self._daily_fee
                    self._email_logs.append(f"[OVERDUE] To: {email} | Week {days_overdue//7} Penalty | Fee: HKD {fee} | Book: {t.book.title}")

    def show_email_logs(self):
        self._auto_scan_emails()
        print("\n=== Automated Email Logs ===")
        if not self._email_logs: print("No alerts for today.")
        for i, log in enumerate(self._email_logs, 1): print(f"{i}. {log}")
