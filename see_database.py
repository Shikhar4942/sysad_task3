import sqlite3

def view_table(table_name):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

if __name__ == '__main__':
    print("Viewing Users Table:")
    view_table('users')
    print("\nViewing Questions Table:")
    view_table('questions')
    print("\nViewing Leaderboard Table:")
    view_table('leaderboard')
