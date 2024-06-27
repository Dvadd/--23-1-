from library_module import Book, StudentCard

def read_books_from_file(filename):
    books = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                books.append(Book.from_string(line))
            except ValueError as e:
                print(e)
    return books

def write_books_to_file(filename, books):
    with open(filename, 'w', encoding='utf-8') as file:
        for book in books:
            file.write(book.to_string() + '\n')

def read_student_cards_from_file(filename):
    cards = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                cards.append(StudentCard.from_string(line))
            except ValueError as e:
                print(e)
    return cards

def write_student_cards_to_file(filename, cards):
    with open(filename, 'w', encoding='utf-8') as file:
        for card in cards:
            file.write(card.to_string() + '\n')
