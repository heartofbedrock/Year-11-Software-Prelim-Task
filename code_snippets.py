#Printing a text
print("Hello World!")

#Creating an array, adding a number to it and then printing the array
array = []
array.append(1)
print(array)

#Conditional (if/else) statement
number = 7
if number % 2 == 0:
    print(f"{number} is even")
else:
    print(f"{number} is odd")    # 7 is odd

#Looping through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print("I like", fruit)

#While loop with a counter
count = 0
while count < 5:
    print("Count is", count)
    count += 1

#Defining and calling a function
def greet(name):
    """Return a greeting for the given name."""
    return f"Hello, {name}!"

message = greet("Alice")
print(message)

#Working with a dictionary
person = {"name": "Bob", "age": 25}
print(person["name"])
person["age"] += 1
print(person)

#List comprehension
squares = [i**2 for i in range(6)]
print(squares)

#Reading input from the user
user_input = input("Enter something: ")
print("You entered:", user_input)

# Using the random model to play a game of rock paper scissors
import random

def play_game():
    choices = ['rock', 'paper', 'scissors']
    computer_choice = random.choice(choices)
    
    user_choice = input("Enter your choice (rock, paper, scissors): ").lower().strip()
    
    if user_choice not in choices:
        print("Invalid choice. Please choose rock, paper, or scissors.")
        return
    
    print(f"Computer chose: {computer_choice}")
    
    if user_choice == computer_choice:
        print("It's a tie!")
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'paper' and computer_choice == 'rock') or \
         (user_choice == 'scissors' and computer_choice == 'paper'):
        print("You win!")
    else:
        print("You lose!")

if __name__ == '__main__':
    play_game()

