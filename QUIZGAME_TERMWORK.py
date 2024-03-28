import requests #imported request for fetching the questions from api
import tkinter as tk #imported tkinter for login and result 
from tkinter import messagebox

class Quiz:
    def __init__(self):
        self.score = 0 #initializing score variable 
##
## it fetched questions from API
# API is generated by opendb trivia api 
#also it return jason format data 
    def fetch_questions_from_api(self):
        api_url = "https://opentdb.com/api.php?amount=10&difficulty=easy"

        response = requests.get(api_url) #get request sent to the url
        try:
        #A status code of 200 indicates a successful request. HTTP status code 200 typically means "OK."
            if response.status_code == 200:
                data = response.json() #this method convers json data into dictionary
                questions = data["results"]
                return questions
            else:
                print("Failed to fetch questions from the API.")
                return 
        except Exception as e:
            print(e)
##
    def start_quiz(self):
        
        #stores value of questions into question variable
        self.questions = self.fetch_questions_from_api()
        if not self.questions:
            return #returns empty if questions not found
##
        for i, q in enumerate(self.questions, 1):            
            print(f"Question {i}: {q['question']}")#prints the questions to the user.
            #choices" will have all the possible answer options for the current question.
            choices = q["incorrect_answers"] + [q["correct_answer"]] 

            #his line processes each answer choice, encoding it as UTF-8 and then decoding it using "unicode_escape." 
            #This is a common operation to handle character encoding and escape sequences special character in text data.
            choices = [choice.encode("utf-8").decode("unicode_escape") for choice in choices]
            choices.sort()  # Shuffle the answer choices

            # #enumerate this iterate thai sake choices ma and proper print thai2
            for i, choice in enumerate(choices, 1):
                print(f"{i}. {choice}")
                #display the answer choices 
                #allows you to create a formatted string with dynamic content without
                #the need for explicit concatenation or string formatting functions.

            userans = input("Enter the number of your answer: ")
            if userans.isdigit():
                userans = int(userans)
                if 1 <= userans <= len(choices): #there should be only one anser
                    if choices[userans - 1] == q["correct_answer"]:
                        print("Correct!\n")
                        self.score += 1
                    else:
                        print("Wrong answer!\n")
                else:
                    print("Invalid input. Please enter a valid choice.\n")
            else:
                print("Invalid input. Please enter a number.\n")

        self.show_result()
##
    def show_result(self):
        try:
            #displays the result
            tot_que = len(self.questions)
            print(f"Quiz completed! Your score is: {self.score}/{tot_que}") 
            messagebox.showinfo("End",f"Your Score, {self.score}/{tot_que}")  
        except Exception as e:
            print(e) 
        

##    
    def login(self):
        try:
            #tk manages all button, labels and textbox
            self.login_window = tk.Tk()
            self.login_window.title("Login")

            #using simple label and textbox for username 
            self.ulabel = tk.Label(self.login_window, text="Username:")
            self.ulabel.pack()

            self.u_txtbox = tk.Entry(self.login_window)
            self.u_txtbox.pack()

            self.plabel = tk.Label(self.login_window, text="Password:")
            self.plabel.pack()

            #password hidden char is * so value of show is *
            self.p_txtbox = tk.Entry(self.login_window, show="*")  # Show asterisks for password
            self.p_txtbox.pack()

            #button for login and calling the function check_login on click tp verify the details 
            self.login_button = tk.Button(self.login_window, text="Login", command=self.check_login)
            self.login_button.pack()

            self.login_window.mainloop()
        except Exception as e:
            print(e)
    
##
    def check_login(self):
        try:
            username = self.u_txtbox.get()
            password = self.p_txtbox.get()

            user_data = {
                "dishant": "123",
                "ram": "jaishriram",
                "krishna": "jaishrikrishna",
            }
    
            if username in user_data and user_data[username] == password:
                messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                self.login_window.destroy()  # Close the login window and enter the quiz method 
                self.start_quiz()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
        except Exception as e:
            print(e)
##
quiz = Quiz() #creatign objecvt of quiz class 
q = quiz.login()
if q == True:
    quiz.start_quiz()
