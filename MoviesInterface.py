# name: Elisabeth Oguntona
# date: 05/15/2025
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 5

import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Movies')
def get_table():
    """Return a reference to the DynamoDB Movies table."""
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    return dynamodb.Table("Movies")

def print_movie(movie):
    title = movie.get("Title", "Unknown Title")
    year = movie.get("Year", "Unknown Year")
    ratings = movie.get("Ratings", "No ratings")
    genre = movie.get("Genre", "No genre listed")

    print(f"  Title  : {title}")
    print(f"  Year   : {year}")
    print(f"  Ratings: {ratings}")
    print(f"  Genre  : {genre}")
    print()



def create_movie():
    title = input("Enter movie title: ")
    year = input("Enter year: ")
    table = get_table()
    table.put_item(
        Item={
            'Title': title,
            'Year': year,
            'Ratings': []
        }
    )
    print(f"'{title}' added successfully!")

def print_all_movies():
    """Scan the entire Movies table and print each item."""
    table = get_table()
    
    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No movies found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} movie(s):\n")
    for movie in items:
        print_movie(movie)

def update_rating():
    try:
        title = input("What is the movie title? ")
        rating = int(input("What is the rating (integer): "))
        table = get_table()
        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Ratings = list_append(Ratings, :r)",
            ExpressionAttributeValues={':r': [rating]}
        )
        print(f"Rating {rating} added to '{title}' successfully!")
    except:
        print("error in updating movie rating")

def delete_movie():
    title = input("Enter the movie title to delete: ")
    table = get_table()
    table.delete_item(Key={"Title": title})
    print(f"'{title}' deleted successfully!")

def query_movie():
    """
    Prompt user for a Movie Title.
    Print out the average of all ratings in the movie's Ratings list.
    """
    print("query movie")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new movie")
    print("Press R: to READ all movies")
    print("Press U: to UPDATE a movie (add a review)")
    print("Press D: to DELETE a movie")
    print("Press Q: to QUERY a movie's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_movie()
        elif input_char.upper() == "R":
            print_all_movies()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_movie()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
