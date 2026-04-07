from core.library_system import LibrarySystem
from utils.barcode_generator import generate_barcode

def main():
    library = LibrarySystem()
    print("=== OOP Library Management System ===")
    print("Demonstrating: Abstraction, Inheritance, Encapsulation, Polymorphism, Composition\n")

    while True:
        print("\n--- Main Menu ---")
        print("1. Add Student")
        print("2. Add Book")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Show All Students")
        print("6. Show All Books")
        print("7. Search Book by Barcode")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            sid = input("Enter Student ID: ")
            name = input("Enter Student Name: ")
            library.add_student(sid, name)

        elif choice == "2":
            isbn = input("Enter ISBN: ")
            title = input("Enter Book Title: ")
            qty = int(input("Enter Quantity: ") or 1)
            barcode = generate_barcode()
            library.add_book(isbn, title, barcode, qty)

        elif choice == "3":
            sid = input("Enter Student ID: ")
            barcode = input("Enter Book Barcode: ")
            library.borrow_book(sid, barcode)

        elif choice == "4":
            barcode = input("Enter Book Barcode to return: ")
            fee = float(input("Enter fee paid (0 if none): ") or 0)
            library.return_book(barcode, fee)

        elif choice == "5":
            library.show_all_students()

        elif choice == "6":
            library.show_all_books()

        elif choice == "7":
            barcode = input("Enter Barcode: ")
            book = library.search_book(barcode)
            if book:
                print(book.display_info())
            else:
                print("Book not found!")

        elif choice == "0":
            print("Thank you for using the Library System!")
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
