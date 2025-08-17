#CatchupSession.py

#review OOP - Inheritance

#from inheritance import Book


class Animal:
    def __init__(self, name) :
        self.name = name

animal1 = Animal("Dog")
animal2 = Animal("Cat")

print(type([animal1, animal2]))
print(animal1.name)
print(animal2.name)

class Book:
    def __init__(self, title, author, publication_date, price):
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.price = price

    def present(self):
        print(f'Title: {self.title}')
        print(f'Author: {self.author}')
        print(f'Publication date: {self.publication_date}')
        print(f'Price: {self.price}')

book1 = Book("1984", "George Orwell", "1948", 100)
print(book1.title)
print(book1.author)
print(book1.publication_date)

book1.present()
Book.present(book1)

class Fiction(Book):
    def __init__(self, title, author, publication_date, price, is_awsome):
        super().__init__(title, author, publication_date, price)
        self.genre = 'Fiction'
        self.is_awsome = is_awsome
    def present(self):
        super().present()
        print(f'Publication date: {self.publication_date}')
        print(f'Price: {self.price}')
        if self.is_awsome:
            print(f'Genre: {self.genre}, \n is awsome ? {self.is_awsome}')
        else:
            print(f' This book is shit ! ')

book2 = Fiction("Contact", "Carl Sagan", "1995", 150, True)
book2.present()

book3 = Fiction("Harry Potter", "J.K. Rowling", "1998", 12.5, False)
book3.present()

