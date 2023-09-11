import sqlite3

# Read the file and copy content to a list
with open('stephen_king_adaptations.txt', 'r') as file:
    stephen_king_adaptations_list = file.readlines()

# Establish connection with SQLite database
connection = sqlite3.connect('stephen_king_adaptations.db')
cursor = connection.cursor()

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table
                  (movieID INTEGER PRIMARY KEY AUTOINCREMENT,
                   movieName TEXT,
                   movieYear INTEGER,
                   imdbRating REAL)''')

# Insert data into table
for line in stephen_king_adaptations_list:
    movie = line.strip().split(',')
    cursor.execute('''INSERT INTO stephen_king_adaptations_table
                      (movieName, movieYear, imdbRating)
                      VALUES (?, ?, ?)''', (movie[1], int(movie[2]), float(movie[3])))

# Commit changes to the database
connection.commit()

# Search option loop
while True:
    print("\nSearch options:")
    print("1. Movie name")
    print("2. Movie year")
    print("3. Movie rating")
    print("4. STOP")

    option = input("Enter your choice (1-4): ")

    if option == '1':
        movie_name = input("Enter the movie name: ")
        cursor.execute('''SELECT * FROM stephen_king_adaptations_table
                          WHERE movieName LIKE ?''', (f'%{movie_name}%',))
        movies = cursor.fetchall()

        if movies:
            for movie in movies:
                print(f"Movie Name: {movie[1]}")
                print(f"Year: {movie[2]}")
                print(f"IMDB Rating: {movie[3]}")
        else:
            print("No such movie exists in our database")

    elif option == '2':
        movie_year = input("Enter the movie year: ")
        cursor.execute('''SELECT * FROM stephen_king_adaptations_table
                          WHERE movieYear = ?''', (int(movie_year),))
        movies = cursor.fetchall()

        if movies:
            for movie in movies:
                print(f"Movie Name: {movie[1]}")
                print(f"Year: {movie[2]}")
                print(f"IMDB Rating: {movie[3]}")
        else:
            print("No movies were found for that year in our database.")

    elif option == '3':
        movie_rating = input("Enter the minimum IMDB rating: ")
        cursor.execute('''SELECT * FROM stephen_king_adaptations_table
                          WHERE imdbRating >= ?''', (float(movie_rating),))
        movies = cursor.fetchall()

        if movies:
            for movie in movies:
                print(f"Movie Name: {movie[1]}")
                print(f"Year: {movie[2]}")
                print(f"IMDB Rating: {movie[3]}")
        else:
            print("No movies at or above that rating were found in the database.")

    elif option == '4':
        break

# Close the connection
connection.close()