class Book:
    def __init__(self, isbn, title, barcode, categories, quantity):
        self.isbn = isbn
        self.title = title
        self.barcode = barcode
        self.categories = categories
        self.total_quantity = int(quantity)      
        self.available_quantity = int(quantity)  
        self.borrow_count = 0
