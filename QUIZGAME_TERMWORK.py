import requests
import tkinter as tk
from tkinter import messagebox


class Quiz:
    def __init__(self):
        self.score = 0
        self.username = None

    def fetch_questions_from_api(self):
        api_url = "https://opentdb.com/api.php?amount=10&difficulty=easy"

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                return data["results"]
            else:
                print("Failed to fetch questions from the API.")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def start_quiz(self):
        self.questions = self.fetch_questions_from_api()
        if not self.questions:
            return

        for i, q in enumerate(self.questions, 1):
            print(f"Question {i}: {q['question']}")
            choices = q["incorrect_answers"] + [q["correct_answer"]]
            choices = [choice.encode("utf-8").decode("unicode_escape") for choice in choices]
            choices.sort()

            for i, choice in enumerate(choices, 1):
                print(f"{i}. {choice}")

            user_answer = input("Enter the number of your answer: ")
            if user_answer.isdigit():
                user_answer = int(user_answer)
                if 1 <= user_answer <= len(choices):
                    if choices[user_answer - 1] == q["correct_answer"]:
                        print("Correct!\n")
                        self.score += 1
                    else:
                        print("Wrong answer!\n")
                else:
                    print("Invalid input. Please enter a valid choice (1-{})".format(len(choices)))
            else:
                print("Invalid input. Please enter a number.\n")

        self.show_result()

    def show_result(self):
        try:
            total_questions = len(self.questions)
            print(f"Quiz completed! Your score is: {self.score}/{total_questions}")
            messagebox.showinfo("End", f"Your Score, {self.score}/{total_questions}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def login(self):
        login_window = tk.Tk()
        login_window.title("Login")

        username_label = tk.Label(login_window, text="Username:")
        username_label.pack()

        username_textbox = tk.Entry(login_window)
        username_textbox.pack()

        password_label = tk.Label(login_window, text="Password:")
        password_label.pack()

        password_textbox = tk.Entry(login_window, show="*")  # Show asterisks for password
        password_textbox.pack()

        def check_login():
            username = username_textbox.get()
            password = password_textbox.get()

            user_data = {
                "dishant": "123",
                "ram": "jaishriram",
                "krishna": "jaishrikrishna",
            }

            if username in user_data and user_data[username] == password:
                self.username = username
                messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                login_window.destroy()
                self.start_quiz()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")

        login_button = tk.Button(login_window, text="Login", command=check_login)
        login_button.pack()

        login_window.mainloop()

        return self.username is not None  # Return True if login successful, False otherwise


if __name__ == "__main__":
    quiz = Quiz()
    if quiz.login():
        quiz.start_quiz()

