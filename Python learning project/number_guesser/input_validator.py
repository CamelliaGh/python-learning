def validate_input(num, start, end):
        if  type(num) == str:
            if (num == 'q'):
                    print("Game is over!")
                    return False
            elif not num.isdigit():
                    print("Input is not a number")
                    return False
        user_guess = int(num)
        if (user_guess < start or user_guess > end):
                print("Number should be between 0 to 100")
                return False
        return True    
    
    
if __name__ == '__main__':
    print(validate_input('a',0, 100))    