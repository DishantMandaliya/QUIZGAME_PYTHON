import requests
import tkinter as tk
from tkinter import messagebox
import csv
import random

class Quiz:
    def __init__(self):
        self.score = 0
        self.username = None
        self.current_question_index = 0  # Track the index of the current question
        self.questions = []

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

        self.quiz_window = tk.Tk()
        self.quiz_window.title("Quiz")

        self.question_label = tk.Label(self.quiz_window, text="", font=("Arial", 16))
        self.question_label.pack(padx=10, pady=10)

        self.answer_vars = []
        for i in range(4):  # Assuming 4 answer choices
            self.answer_vars.append(tk.IntVar(value=0))  # Store answer selection (0 for not selected)

        self.answer_buttons = []
        for i in range(4):
            answer_button = tk.Radiobutton(
                self.quiz_window, text="", variable=self.answer_vars[i], value=i+1
            )
            answer_button.pack(anchor="w", padx=20)
            self.answer_buttons.append(answer_button)

        self.submit_button = tk.Button(self.quiz_window, text="Submit Answer", command=self.check_answer)
        self.submit_button.pack(pady=10)

        self.next_button = tk.Button(self.quiz_window, text="Next Question", state="disabled", command=self.next_question)
        self.next_button.pack(pady=10)

        self.show_question(self.current_question_index)  # Show the first question
        self.quiz_window.mainloop()

    def show_question(self, question_index):
        if not self.questions:
            return

        question = self.questions[question_index]
        self.question_label.config(text=question["question"])

        # Shuffle the answer choices
        answer_choices = [question["correct_answer"]] + question["incorrect_answers"]
        random.shuffle(answer_choices)

        for i in range(4):
            self.answer_buttons[i].config(text=answer_choices[i])
            self.answer_buttons[i].config(state="normal")  # Enable all buttons

        self.submit_button.config(state="normal")  # Enable submit button
        self.next_button.config(state="disabled")  # Disable next button

    def check_answer(self):
        if not self.questions:
            return

        selected_answer = sum(var.get() for var in self.answer_vars)
        if selected_answer == 0:
            messagebox.showinfo("Selection Required", "Please select an answer.")
            return

        correct_answer = self.questions[self.current_question_index]["correct_answer"]
        user_answer = self.answer_buttons[selected_answer - 1].cget("text")

        if user_answer == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct!", "Your answer is correct.")
        else:
            messagebox.showinfo("Incorrect", f"Incorrect. The correct answer is: {correct_answer}")

        # Disable buttons and enable next button
        for button in self.answer_buttons:
            button.config(state="disabled")
        self.submit_button.config(state="disabled")
        self.next_button.config(state="normal")

    def next_question(self):
        if not self.questions:
            return

        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.show_question(self.current_question_index)
        else:
            messagebox.showinfo("End of Quiz", f"Quiz ended. Your score: {self.score}")

# Usage
quiz = Quiz()
quiz.start_quiz()
