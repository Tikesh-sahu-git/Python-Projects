import random

def guess_the_number():
    # Set up the game
    low = 1
    high = 50
    secret = random.randint(low, high)
    guesses = 0
    max_guesses = 5
    
    print(f"Guess my number between {low} and {high}!")
    print(f"You have {max_guesses} tries.")
    
    # Game loop
    while guesses < max_guesses:
        try:
            guess = int(input("Your guess: "))
            guesses += 1
            
            if guess == secret:
                print(f"Correct! You got it in {guesses} tries!")
                return
            elif guess < secret:
                print("Too low!")
            else:
                print("Too high!")
                
            print(f"Tries left: {max_guesses - guesses}")
            
        except:
            print("Please enter a number!")
    
    # Ran out of guesses
    print(f"Game over! The number was {secret}.")

# Start the game
guess_the_number()
