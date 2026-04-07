from abc import ABC, abstractmethod
from datetime import datetime

class Person(ABC):
    """Abstract Base Class - Abstraction"""
    
    def __init__(self, person_id: str, name: str):
        self._person_id = person_id     
        self._name = name
        self._created_at = datetime.now()

    @property
    def person_id(self):
        return self._person_id

    @property
    def name(self):
        return self._name

    @abstractmethod
    def get_role(self) -> str:
        """Force subclasses to implement this - Abstraction"""
        pass

    def display_info(self) -> str:
        """Can be overridden - Polymorphism"""
        return f"ID: {self.person_id} | Name: {self.name} | Role: {self.get_role()}"
