# Printing a text
print("Hello World!")

# Creating an array, adding a number to it and then printing the array
array = []
array.append(1)
print(array)

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

