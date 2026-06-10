# name: Elisabeth Oguntona
# date: 06/10/2026
# description: CRUD interface for Book table — CS178 Lab 10
# proposed score: 5

import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Book')

def get_table():
    return dynamodb.Table('Book')

def print_book(book):
    print(f"  Title  : {book.get('Title', 'Unknown')}")
    print(f"  Author : {book.get('Author', 'Unknown')}")
    print(f"  Genre  : {book.get('Genre', 'Unknown')}")
    print()

def create_book():
    title = input("Enter book title: ")
    author = input("Enter author: ")
    genre = input("Enter genre: ")
    table = get_table()
    table.put_item(Item={'Title': title, 'Author': author, 'Genre': genre, 'Ratings': []})
    print(f"'{title}' added successfully!")

def read_books():
    table = get_table()
    response = table.scan()
    items = response.get("Items", [])
    if not items:
        print("No books found.")
        return
    print(f"Found {len(items)} book(s):\n")
    for book in items:
        print_book(book)

def update_book():
    try:
        title = input("Enter book title to update: ")
        rating = int(input("Enter rating (integer): "))
        table = get_table()
        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Ratings = list_append(Ratings, :r)",
            ExpressionAttributeValues={':r': [rating]}
        )
        print(f"Rating added to '{title}' successfully!")
    except:
        print("error in updating book rating")

def delete_book():
    title = input("Enter book title to delete: ")
    table = get_table()
    table.delete_item(Key={"Title": title})
    print(f"'{title}' deleted successfully!")

def query_book():
    title = input("Enter book title to query: ")
    table = get_table()
    response = table.get_item(Key={"Title": title})
    book = response.get("Item")
    if not book:
        print("book not found")
        return
    ratings_list = book.get("Ratings", [])
    if len(ratings_list) == 0:
        print("book has no ratings")
        return
    average = sum(ratings_list) / len(ratings_list)
    print(f"Average rating for '{title}': {average:.2f}")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new book")
    print("Press R: to READ all books")
    print("Press U: to UPDATE a book (add a rating)")
    print("Press D: to DELETE a book")
    print("Press Q: to QUERY a book's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_book()
        elif input_char.upper() == "R":
            read_books()
        elif input_char.upper() == "U":
            update_book()
        elif input_char.upper() == "D":
            delete_book()
        elif input_char.upper() == "Q":
            query_book()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()