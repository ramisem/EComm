import sqlite3

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(dbname):
    import sqlite3

    # Connect to the SQLite database (creates the database file if it doesn't exist)
    conn = sqlite3.connect(dbname)

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Example SELECT query
    # cursor.execute('SELECT sql FROM sqlite_master WHERE type=\'table\'')
    # cursor.execute('SELECT * FROM userauths_user')
    cursor.execute('PRAGMA table_info(userauths_user)')
    rows = cursor.fetchall()

    # Process the result
    for row in rows:
        print(row)

    # Close the cursor and connection
    cursor.close()
    conn.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('ecomprj/db.sqlite3')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
