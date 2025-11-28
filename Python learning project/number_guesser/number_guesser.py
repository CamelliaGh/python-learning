import random
import input_validator
class NumberGuesser:
    def __init__(self):
        pass
    
    def validate_input(self, num_str):
        return input_validator.validate_input(num_str,0, 100)
     
    def play(self):
        target_number = random.randint(0, 100)
        while True:
            num_str = input("Guess a number between 0 to 100, unless enter q to quit: ")
            
            if not self.validate_input(num_str):
                continue
            
            user_guess = int(num_str)
            
            
            if (target_number == user_guess):
                print("Congratulation! You nailed it!")
                break
            elif user_guess > target_number:
                print("Wrong, guess again, your number is greater than target number ----") 
            elif user_guess < target_number:
                print("Wrong, guess again, your number is less than target number +++")          
        
    
if __name__ == '__main__':
    number_guesser = NumberGuesser()
    number_guesser.play()    