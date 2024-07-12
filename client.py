
import socket

def client_program():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5555))  

    authenticated = False

    def register():
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        client.send(f'REGISTER|{username}|{password}'.encode('utf-8'))
        print(client.recv(1024).decode('utf-8'))

    def login():
        nonlocal authenticated
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        client.send(f'LOGIN|{username}|{password}'.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        print(response)
        if response == "Login successful.":
            authenticated = True

    def add_question():
        question = input("Enter the question: ")
        opt1 = input("Option 1: ")
        opt2 = input("Option 2: ")
        opt3 = input("Option 3: ")
        opt4 = input("Option 4: ")
        answer = input("Correct option: ")
        client.send(f'ADD|{question}|{opt1}|{opt2}|{opt3}|{opt4}|{answer}'.encode('utf-8'))
        print(client.recv(1024).decode('utf-8'))

    def answer_question():
        qid = input("Enter the question ID you want to answer: ")
        client.send(f'ANSWER|{qid}'.encode('utf-8'))
        question_response = client.recv(1024).decode('utf-8')
        print(question_response)
        answer = input("Your answer: ")
        client.send(f'ANSWER|{qid}|{answer}'.encode('utf-8'))
        print(client.recv(1024).decode('utf-8'))

    def view_leaderboard():
        client.send('LEADERBOARD|'.encode('utf-8'))
        print(client.recv(1024).decode('utf-8'))

    while True:
        if not authenticated:
            print("1. Register")
            print("2. Login")
            choice = input("Select an option: ")
            if choice == '1':
                register()
            elif choice == '2':
                login()
        else:
            print("1. Add Question")
            print("2. Answer Question")
            print("3. View Leaderboard")
            print("4. Disconnect")
            choice = input("Select an option: ")
            if choice == '1':
                add_question()
            elif choice == '2':
                answer_question()
            elif choice == '3':
                view_leaderboard()
            elif choice == '4':
                client.send('DISCONNECT|'.encode('utf-8'))
                break

client_program()
