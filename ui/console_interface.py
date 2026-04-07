def admin_login(library):
    """Admin Login with 3 attempts"""
    attempts = 3
    print("\n" + "="*45 + "\n    HKMU LIBRARY ADMIN LOGIN\n" + "="*45)
    while attempts > 0:
        pwd = input(f"Enter Admin Password ({attempts} left): ")
        if library.login(pwd): return True
        attempts -= 1
        print("❌ Incorrect password.")
    return False

def main_menu(library):
    while True:
        print("\n" + "-"*45)
        print(" 1. Add Student          2. Add Book")
        print(" 3. Borrow Book          4. Return Book")
        print(" 5. Student Status       6. Book Status")
        print(" 7. Dashboards           8. Change Password")
        print(" 9. View All Books       10. Check Email Logs")
        print(" 0. Logout")
        
        choice = input("\nSelect Option (0-10): ").strip()
        
        if choice == "1":
            while True:
                sid = input("Enter 8-digit Student ID: ").strip()
                if len(sid) == 8 and sid.isdigit(): break
                print("❌ Error: SID must be 8 digits.")
            name = input("Enter Name: ")
            library.add_student(sid, name)

        elif choice == "2":
            isbn, title = input("ISBN: "), input("Title: ")
            print("\n[ Available Categories ]")
            cats = library._default_categories
            for i in range(10):
                print(f" {cats[i]:<18} {cats[i+10]}")
            cat = input("\nEnter Category IDs (e.g., 1,4): ")
            qty = input("Quantity: ")
            library.add_book(isbn, title, cat, qty or 1)

        elif choice == "3":
            sid, bid = input("Student ID: "), input("Book Barcode: ")
            library.borrow_book(sid, bid)

        elif choice == "4":
            sid = input("Enter Student ID: ")
            bid = input("Enter Book Barcode: ")
            library.return_book(sid, bid)

        elif choice == "5":
            sid = input("Enter Student ID: ")
            rep = library.get_student_report(sid)
            if rep:
                print(f"\n--- [ Student Status: {rep['name']} ] ---")
                print(f"Student ID: {rep['sid']}")
                print(f"Lifetime Borrows: {rep['total']}")
                print(f"Current Books (Days Left): {', '.join(rep['current']) or 'None'}")
                print(f"Overdue Items: {', '.join(rep['overdue']) or 'None'}")
                print(f"Total Fees: HKD {rep['fee']}")
            else: print("❌ Not found.")

        elif choice == "6":
            print("Hint: Barcode format is 'b000001'")
            bid = input("Enter Barcode: ")
            b = library._books.get(bid)
            if b:
                borrowed = b.total_quantity - b.available_quantity
                
                print(f"\n--- [ Book Detail ] ---")
                print(f"Title:    {b.title}")
                print(f"Barcode:  {b.barcode}")
                print(f"ISBN:     {b.isbn}")
                print(f"Category: {b.categories}")
                print("-" * 25)
                print(f"Current Stock: {b.available_quantity}")
                print(f"Borrowed:      {borrowed}")
                print(f"Total Stock:   {b.total_quantity}")
                print("-" * 25)
            else: 
                print("❌ Book not found.")
        
        elif choice == "7":
            print("\n1. Top 10 Categories | 2. Top 10 Books")
            sub = input("Select Dashboard: ")
            if sub == "1":
                for i, (name, count) in enumerate(library.get_top10_cats(), 1):
                    print(f"{i}. {name:<15} | Borrows: {count}")
            elif sub == "2":
                books = library.get_top10_books()
                if not books: print("📊 No data.")
                else:
                    for i, b in enumerate(books, 1):
                        print(f"{i}. {b.title[:20]:<20} | Borrows: {b.borrow_count}")

        elif choice == "8":
            old = input("Current Password: ")
            new = input("New Password: ")
            if library.change_password(old, new): print("✅ Password changed.")
            else: print("❌ Incorrect current password.")

        elif choice == "9":
            p = 1
            while True:
                items, total_p, count = library.get_paginated_books(p)
                print(f"\n=== Books (Page {p}/{total_p} | Total: {count}) ===")
                print(f"{'Barcode':<10} {'Name':<20} {'ISBN':<12} {'Total':<6} {'Brw':<4}")
                print("-" * 60)
                for b in items:
                    brw = b.total_quantity - b.available_quantity
                    print(f"{b.barcode:<10} {b.title[:18]:<20} {b.isbn:<12} {b.total_quantity:<6} {brw:<4}")
                nav = input("\n[N]ext | [P]rev | [B]ack: ").upper()
                if nav == 'N' and p < total_p: p += 1
                elif nav == 'P' and p > 1: p -= 1
                elif nav == 'B': break

        elif choice == "10": 
            library.show_email_logs()
        
        elif choice == "0": break
