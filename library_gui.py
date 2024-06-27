import tkinter as tk
from tkinter import messagebox, ttk
from library_module import Book, StudentCard
from library_file_handler import read_books_from_file, write_books_to_file, read_student_cards_from_file, write_student_cards_to_file
import json
from datetime import datetime

class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")

        self.books = read_books_from_file("books.txt")
        self.student_cards = read_student_cards_from_file("students.txt")
        self.filtered_books = self.books
        self.filtered_students = self.student_cards

        self.setup_ui()

    def setup_ui(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Manage Books", command=self.show_books_form)
        self.file_menu.add_command(label="Manage Student Cards", command=self.show_student_cards_form)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.show_books_form()

    def show_books_form(self):
        self.clear_frame()

        self.search_label = tk.Label(self.frame, text="Search by")
        self.search_label.grid(row=0, column=0, padx=10, pady=5)

        self.search_option = tk.StringVar()
        self.search_option.set("Title")  # Default value
        self.search_option_menu = tk.OptionMenu(self.frame, self.search_option, "Title", "Author", "Year")
        self.search_option_menu.grid(row=0, column=1, padx=10, pady=5)

        self.search_entry = tk.Entry(self.frame)
        self.search_entry.grid(row=0, column=2, padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self.search_books)  # Bind KeyRelease event to search_books

        self.book_listbox = tk.Listbox(self.frame, width=100, height=20)
        self.book_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        self.book_listbox.bind("<Button-3>", self.show_context_menu)  # Bind right-click to show context menu

        self.update_book_listbox()

        self.add_book_button = tk.Button(self.frame, text="Add Book", command=self.open_add_book_form)
        self.add_book_button.grid(row=2, column=2, padx=10, pady=5, sticky="e")

    def show_student_cards_form(self):
        self.clear_frame()

        self.search_label = tk.Label(self.frame, text="Search by")
        self.search_label.grid(row=0, column=0, padx=10, pady=5)

        self.search_option = tk.StringVar()
        self.search_option.set("Name")  # Default value
        self.search_option_menu = tk.OptionMenu(self.frame, self.search_option, "Name", "ID", "Group", "Overdue", command=self.search_students)
        self.search_option_menu.grid(row=0, column=1, padx=10, pady=5)

        self.search_entry = tk.Entry(self.frame)
        self.search_entry.grid(row=0, column=2, padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self.search_students)  # Bind KeyRelease event to search_students

        self.student_listbox = tk.Listbox(self.frame, width=100, height=20)
        self.student_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        self.student_listbox.bind("<Button-3>", self.show_student_context_menu)  # Bind right-click to show context menu

        self.update_card_listbox()

        self.add_card_button = tk.Button(self.frame, text="Add Student", command=self.open_add_card_form)
        self.add_card_button.grid(row=2, column=2, padx=10, pady=5, sticky="e")

    def search_books(self, event=None):
        search_term = self.search_entry.get().lower()
        search_option = self.search_option.get()

        if search_option == "Title":
            self.filtered_books = [book for book in self.books if search_term in book.title.lower()]
        elif search_option == "Author":
            self.filtered_books = [book for book in self.books if search_term in book.author.lower()]
        elif search_option == "Year":
            self.filtered_books = [book for book in self.books if search_term == str(book.year)]

        self.update_book_listbox()

    def search_students(self, event=None):
        search_term = self.search_entry.get().lower()
        search_option = self.search_option.get()

        if search_option == "Name":
            self.filtered_students = [card for card in self.student_cards if search_term in card.student_name.lower()]
        elif search_option == "ID":
            self.filtered_students = [card for card in self.student_cards if search_term == str(card.id)]
        elif search_option == "Group":
            self.filtered_students = [card for card in self.student_cards if search_term in card.group.lower()]
        elif search_option == "Overdue":
            self.filtered_students = self.get_overdue_students()

        self.update_card_listbox()

    def add_book(self, title, author, year, quantity):
        if not title or not author or not year or not quantity:
            messagebox.showerror("Error", "All fields must be filled out")
            return

        try:
            year = int(year)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Year and Quantity must be integers")
            return

        new_book = Book(id=len(self.books) + 1, title=title, author=author, year=year, quantity=quantity)
        self.books.append(new_book)
        write_books_to_file("books.txt", self.books)
        self.update_book_listbox()

    def add_card(self, name, issue_date, group, borrowed_books):
        if not name or not issue_date or not group:
            messagebox.showerror("Error", "All fields must be filled out")
            return

        new_card = StudentCard(id=len(self.student_cards) + 1, title="Student Card", student_name=name, issue_date=issue_date, group=group, borrowed_books=borrowed_books)
        self.student_cards.append(new_card)
        write_student_cards_to_file("students.txt", self.student_cards)
        self.update_card_listbox()

    def update_book_listbox(self):
        self.book_listbox.delete(0, tk.END)
        for book in self.filtered_books:
            self.book_listbox.insert(tk.END, book.display_info())

    def update_card_listbox(self):
        self.student_listbox.delete(0, tk.END)
        for card in self.filtered_students:
            borrowed_books_info = card.get_borrowed_books_info(self.books)
            borrowed_books_text = ", ".join([f"{book_name} (Due: {due_date})" for book_name, due_date in borrowed_books_info])
            display_text = f"ID: {card.id} | Name: {card.student_name} | Issue Date: {card.issue_date} | Group: {card.group} | Borrowed Books: {borrowed_books_text}"
            self.student_listbox.insert(tk.END, display_text)

    def get_overdue_students(self):
        overdue_students = []
        today = datetime.today().date()

        for student in self.student_cards:
            for book in student.borrowed_books:
                for due_date in book.values():
                    if datetime.strptime(due_date, '%Y-%m-%d').date() < today:
                        if student not in overdue_students:
                            overdue_students.append(student)
                        break  # Exit inner loop once an overdue book is found for this student

        return overdue_students

    def open_add_book_form(self):
        self.add_book_window = tk.Toplevel(self.root)
        self.add_book_window.title("Add Book")

        tk.Label(self.add_book_window, text="Title").grid(row=0, column=0, padx=10, pady=5)
        self.new_book_title_entry = tk.Entry(self.add_book_window)
        self.new_book_title_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.add_book_window, text="Author").grid(row=1, column=0, padx=10, pady=5)
        self.new_book_author_entry = tk.Entry(self.add_book_window)
        self.new_book_author_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.add_book_window, text="Year").grid(row=2, column=0, padx=10, pady=5)
        self.new_book_year_entry = tk.Entry(self.add_book_window)
        self.new_book_year_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.add_book_window, text="Quantity").grid(row=3, column=0, padx=10, pady=5)
        self.new_book_quantity_entry = tk.Entry(self.add_book_window)
        self.new_book_quantity_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(self.add_book_window, text="Add", command=self.confirm_add_book).grid(row=4, column=1, padx=10, pady=10)

    def confirm_add_book(self):
        title = self.new_book_title_entry.get()
        author = self.new_book_author_entry.get()
        year = self.new_book_year_entry.get()
        quantity = self.new_book_quantity_entry.get()
        self.add_book(title, author, year, quantity)
        self.add_book_window.destroy()

    def open_add_card_form(self):
        self.add_card_window = tk.Toplevel(self.root)
        self.add_card_window.title("Add Student")

        tk.Label(self.add_card_window, text="Name").grid(row=0, column=0, padx=10, pady=5)
        self.new_card_name_entry = tk.Entry(self.add_card_window)
        self.new_card_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.add_card_window, text="Issue Date").grid(row=1, column=0, padx=10, pady=5)
        self.new_card_issue_date_entry = tk.Entry(self.add_card_window)
        self.new_card_issue_date_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.add_card_window, text="Group").grid(row=2, column=0, padx=10, pady=5)
        self.new_card_group_entry = tk.Entry(self.add_card_window)
        self.new_card_group_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.add_card_window, text="Borrowed Books").grid(row=3, column=0, padx=10, pady=5)
        self.borrowed_books_frame = tk.Frame(self.add_card_window)
        self.borrowed_books_frame.grid(row=3, column=1, padx=10, pady=5)
        self.borrowed_books = []

        self.add_borrowed_book_row()

        tk.Button(self.add_card_window, text="Add Book", command=self.add_borrowed_book_row).grid(row=4, column=1, padx=10, pady=5)
        tk.Button(self.add_card_window, text="Add", command=self.confirm_add_card).grid(row=5, column=1, padx=10, pady=10)

    def add_borrowed_book_row(self, book_var=None, date_var=None):
        book_var = book_var or tk.StringVar()
        date_var = date_var or tk.StringVar()

        row_frame = tk.Frame(self.borrowed_books_frame)
        row_frame.pack(fill=tk.X, pady=2)

        book_menu = ttk.Combobox(row_frame, textvariable=book_var, values=[book.title for book in self.books])
        book_menu.pack(side=tk.LEFT, fill=tk.X, expand=True)

        date_entry = tk.Entry(row_frame, textvariable=date_var)
        date_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        delete_button = tk.Button(row_frame, text="❌", command=lambda: self.delete_borrowed_book_row(row_frame))
        delete_button.pack(side=tk.LEFT, padx=5)

        self.borrowed_books.append((book_var, date_var, row_frame))

    def delete_borrowed_book_row(self, row_frame):
        row_frame.destroy()
        self.borrowed_books = [entry for entry in self.borrowed_books if entry[2] != row_frame]

    def confirm_add_card(self):
        name = self.new_card_name_entry.get()
        issue_date = self.new_card_issue_date_entry.get()
        group = self.new_card_group_entry.get()
        borrowed_books = [{str(self.books[i].id): date_var.get()} for i, (book_var, date_var, _) in enumerate(self.borrowed_books) if book_var.get() and date_var.get()]
        self.add_card(name, issue_date, group, borrowed_books)
        self.add_card_window.destroy()

    def show_context_menu(self, event):
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Edit", command=lambda: self.edit_book(event))
        context_menu.add_command(label="Delete", command=lambda: self.delete_book(event))
        context_menu.post(event.x_root, event.y_root)

    def show_student_context_menu(self, event):
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Edit", command=lambda: self.edit_card(event))
        context_menu.add_command(label="Delete", command=lambda: self.delete_card(event))
        context_menu.post(event.x_root, event.y_root)

    def edit_book(self, event):
        selected_index = self.book_listbox.curselection()
        if not selected_index:
            return
        selected_index = selected_index[0]
        selected_book = self.filtered_books[selected_index]

        self.edit_book_window = tk.Toplevel(self.root)
        self.edit_book_window.title("Edit Book")

        tk.Label(self.edit_book_window, text="Title").grid(row=0, column=0, padx=10, pady=5)
        self.edit_book_title_entry = tk.Entry(self.edit_book_window)
        self.edit_book_title_entry.grid(row=0, column=1, padx=10, pady=5)
        self.edit_book_title_entry.insert(0, selected_book.title)

        tk.Label(self.edit_book_window, text="Author").grid(row=1, column=0, padx=10, pady=5)
        self.edit_book_author_entry = tk.Entry(self.edit_book_window)
        self.edit_book_author_entry.grid(row=1, column=1, padx=10, pady=5)
        self.edit_book_author_entry.insert(0, selected_book.author)

        tk.Label(self.edit_book_window, text="Year").grid(row=2, column=0, padx=10, pady=5)
        self.edit_book_year_entry = tk.Entry(self.edit_book_window)
        self.edit_book_year_entry.grid(row=2, column=1, padx=10, pady=5)
        self.edit_book_year_entry.insert(0, selected_book.year)

        tk.Label(self.edit_book_window, text="Quantity").grid(row=3, column=0, padx=10, pady=5)
        self.edit_book_quantity_entry = tk.Entry(self.edit_book_window)
        self.edit_book_quantity_entry.grid(row=3, column=1, padx=10, pady=5)
        self.edit_book_quantity_entry.insert(0, selected_book.quantity)

        tk.Button(self.edit_book_window, text="Save", command=lambda: self.confirm_edit_book(selected_index)).grid(row=4, column=1, padx=10, pady=10)

    def confirm_edit_book(self, index):
        title = self.edit_book_title_entry.get()
        author = self.edit_book_author_entry.get()
        year = self.edit_book_year_entry.get()
        quantity = self.edit_book_quantity_entry.get()

        if not title or not author or not year or not quantity:
            messagebox.showerror("Error", "All fields must be filled out")
            return

        try:
            year = int(year)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Year and Quantity must be integers")
            return

        self.books[index].title = title
        self.books[index].author = author
        self.books[index].year = year
        self.books[index].quantity = quantity
        write_books_to_file("books.txt", self.books)
        self.update_book_listbox()
        self.edit_book_window.destroy()

    def delete_book(self, event):
        selected_index = self.book_listbox.curselection()
        if not selected_index:
            return
        selected_index = selected_index[0]
        del self.books[selected_index]
        write_books_to_file("books.txt", self.books)
        self.update_book_listbox()

    def edit_card(self, event):
        selected_index = self.student_listbox.curselection()
        if not selected_index:
            return
        selected_index = selected_index[0]
        selected_card = self.filtered_students[selected_index]

        self.edit_card_window = tk.Toplevel(self.root)
        self.edit_card_window.title("Edit Student")

        tk.Label(self.edit_card_window, text="Name").grid(row=0, column=0, padx=10, pady=5)
        self.edit_card_name_entry = tk.Entry(self.edit_card_window)
        self.edit_card_name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.edit_card_name_entry.insert(0, selected_card.student_name)

        tk.Label(self.edit_card_window, text="Issue Date").grid(row=1, column=0, padx=10, pady=5)
        self.edit_card_issue_date_entry = tk.Entry(self.edit_card_window)
        self.edit_card_issue_date_entry.grid(row=1, column=1, padx=10, pady=5)
        self.edit_card_issue_date_entry.insert(0, selected_card.issue_date)

        tk.Label(self.edit_card_window, text="Group").grid(row=2, column=0, padx=10, pady=5)
        self.edit_card_group_entry = tk.Entry(self.edit_card_window)
        self.edit_card_group_entry.grid(row=2, column=1, padx=10, pady=5)
        self.edit_card_group_entry.insert(0, selected_card.group)

        tk.Label(self.edit_card_window, text="Borrowed Books").grid(row=3, column=0, padx=10, pady=5)
        self.borrowed_books_frame = tk.Frame(self.edit_card_window)
        self.borrowed_books_frame.grid(row=3, column=1, padx=10, pady=5)
        self.borrowed_books = []

        for book in selected_card.borrowed_books:
            for book_id, due_date in book.items():
                book_var = tk.StringVar(value=next((b.title for b in self.books if b.id == int(book_id)), ""))
                date_var = tk.StringVar(value=due_date)
                self.add_borrowed_book_row(book_var, date_var)

        tk.Button(self.edit_card_window, text="Add Book", command=self.add_borrowed_book_row).grid(row=4, column=1, padx=10, pady=5)
        tk.Button(self.edit_card_window, text="Save", command=lambda: self.confirm_edit_card(selected_index)).grid(row=5, column=1, padx=10, pady=10)

    def confirm_edit_card(self, index):
        name = self.edit_card_name_entry.get()
        issue_date = self.edit_card_issue_date_entry.get()
        group = self.edit_card_group_entry.get()
        borrowed_books = [{str(self.books[i].id): date_var.get()} for i, (book_var, date_var, _) in enumerate(self.borrowed_books) if book_var.get() and date_var.get()]

        if not name or not issue_date or not group:
            messagebox.showerror("Error", "All fields must be filled out")
            return

        self.student_cards[index].student_name = name
        self.student_cards[index].issue_date = issue_date
        self.student_cards[index].group = group
        self.student_cards[index].borrowed_books = borrowed_books
        write_student_cards_to_file("students.txt", self.student_cards)
        self.update_card_listbox()
        self.edit_card_window.destroy()

    def delete_card(self, event):
        selected_index = self.student_listbox.curselection()
        if not selected_index:
            return
        selected_index = selected_index[0]
        del self.student_cards[selected_index]
        write_student_cards_to_file("students.txt", self.student_cards)
        self.update_card_listbox()

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.pack_forget()
        self.frame.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
