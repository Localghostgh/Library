import json
import os

BOOKS_FILE = 'books.json'

class Book:
    """Класс для представления книги."""

    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        """Преобразует объект книги в словарь."""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }

    @staticmethod
    def from_dict(data: dict):
        """Создает объект книги из словаря."""
        return Book(data['id'], data['title'], data['author'], data['year'], data['status'])

class Library:
    """Класс для управления библиотекой книг."""

    def __init__(self):
        self.books = []
        self.load_books()

    def load_books(self):
        """Загружает книги из файла."""
        if os.path.exists(BOOKS_FILE):
            with open(BOOKS_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.books = [Book.from_dict(book) for book in data]

    def save_books(self):
        """Сохраняет книги в файл."""
        with open(BOOKS_FILE, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        """Добавляет новую книгу в библиотеку."""
        new_id = len(self.books) + 1  # Генерация уникального ID
        new_book = Book(new_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        print(f"Книга '{title}' добавлена в библиотеку.")

    def remove_book(self, book_id: int):
        """Удаляет книгу по ID."""
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f"Книга с ID {book_id} удалена.")
                return
        print(f"Книга с ID {book_id} не найдена.")

    def search_books(self, query: str):
        """Ищет книги по названию, автору или году издания."""
        results = [book for book in self.books if (query.lower() in book.title.lower() or
                                                   query.lower() in book.author.lower() or
                                                   query == str(book.year))]
        return results

    def display_books(self):
        """Отображает все книги в библиотеке."""
        if not self.books:
            print("Библиотека пуста.")
            return
        print("Список книг в библиотеке:")
        for book in self.books:
            print(
                f"ID: {book.id}, Название: '{book.title}', Автор: '{book.author}', Год: {book.year}, Статус: {book.status}")

    def change_status(self, book_id: int, new_status: str):
        """Изменяет статус книги по ID."""
        for book in self.books:
            if book.id == book_id:
                if new_status in ["в наличии", "выдана"]:
                    book.status = new_status
                    self.save_books()
                    print(f"Статус книги с ID {book_id} изменен на '{new_status}'.")
                else:
                    print("Неверный статус. Используйте 'в наличии' или 'выдана'.")
                return
        print(f"Книга с ID {book_id} не найдена.")

def main():
    library = Library()

    while True:
        print("\nВыберите действие:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Введите номер действия: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания: "))
            library.add_book(title, author, year)

        elif choice == '2':
            book_id = int(input("Введите ID книги для удаления: "))
            library.remove_book(book_id)

        elif choice == '3':
            query = input("Введите название, автора или год для поиска: ")
            results = library.search_books(query)
            if results:
                print("Найденные книги:")
                for book in results:
                    print(
                        f"ID: {book.id}, Название: '{book.title}', Автор: '{book.author}', Год: {book.year}, Статус: {book.status}")
            else:
                print("Книги не найдены.")

        elif choice == '4':
            library.display_books()

        elif choice == '5':
            book_id = int(input("Введите ID книги для изменения статуса: "))
            new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            library.change_status(book_id, new_status)

        elif choice == '6':
            print("Выход из программы.")
            break

        else:
            print("Неверный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()

