import json

class Item:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def display_info(self):
        raise NotImplementedError("Subclasses should implement this method")


class Book(Item):
    def __init__(self, id, title, author, year, quantity):
        super().__init__(id, title)
        self.author = author
        self.year = year
        self.quantity = quantity

    def display_info(self):
        return f"ID: {self.id} | Title: {self.title} | Author: {self.author} | Year: {self.year} | Quantity: {self.quantity}"

    @staticmethod
    def from_string(book_str):
        parts = book_str.strip().split(" | ")
        if len(parts) != 5:
            raise ValueError(f"Invalid book string: {book_str}")
        return Book(int(parts[0]), parts[1], parts[2], int(parts[3]), int(parts[4]))

    def to_string(self):
        return f"{self.id} | {self.title} | {self.author} | {self.year} | {self.quantity}"

class StudentCard(Item):
    def __init__(self, id, title, student_name, issue_date, group, borrowed_books=None):
        super().__init__(id, title)
        self.student_name = student_name
        self.issue_date = issue_date
        self.group = group
        self.borrowed_books = borrowed_books if borrowed_books is not None else []

    def display_info(self):
        return f"ID: {self.id} | Name: {self.student_name} | Issue Date: {self.issue_date} | Group: {self.group}"

    @staticmethod
    def from_string(card_str):
        parts = card_str.strip().split(" | ")
        if len(parts) != 5:
            raise ValueError(f"Invalid card string: {card_str}")
        borrowed_books = json.loads(parts[4])
        return StudentCard(int(parts[0]), "Student Card", parts[1], parts[2], parts[3], borrowed_books)

    def to_string(self):
        return f"{self.id} | {self.student_name} | {self.issue_date} | {self.group} | {json.dumps(self.borrowed_books)}"

    def get_borrowed_books_info(self, books):
        borrowed_books_info = []
        for book in self.borrowed_books:
            for book_id, due_date in book.items():
                book_name = next((b.title for b in books if b.id == int(book_id)), "Unknown")
                borrowed_books_info.append((book_name, due_date))
        return borrowed_books_info
