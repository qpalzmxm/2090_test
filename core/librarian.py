from core.person import Person

class Librarian(Person):
    """Another subclass demonstrating Inheritance & Polymorphism"""

    def __init__(self, librarian_id: str, name: str):
        super().__init__(librarian_id, name)

    def get_role(self) -> str:
        return "Librarian"

    def display_info(self) -> str:
        return super().display_info() + " (Admin Access)"
