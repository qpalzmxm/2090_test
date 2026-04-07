from datetime import datetime

class Book:
    """Strong Encapsulation with private attributes and properties"""

    def __init__(self, isbn: str, title: str, barcode: str, quantity: int = 1):
        self.__isbn = isbn                    # Private
        self.__title = title
        self.__barcode = barcode
        self.__quantity = quantity
        self.__available = quantity
        self.__added_date = datetime.now()

    @property
    def isbn(self): return self.__isbn
    @property
    def title(self): return self.__title
    @property
    def barcode(self): return self.__barcode
    @property
    def available(self): return self.__available

    def borrow_one(self) -> bool:
        if self.__available > 0:
            self.__available -= 1
            return True
        return False

    def return_one(self) -> bool:
        if self.__available < self.__quantity:
            self.__available += 1
            return True
        return False

    def display_info(self) -> str:
        return (f"Title: {self.title} | ISBN: {self.isbn} | "
                f"Barcode: {self.barcode} | Available: {self.available}/{self.__quantity}")
