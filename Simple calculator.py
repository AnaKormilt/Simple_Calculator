# The following program represents the simple calculator, which asks for the name of the file, where the results will be saved, 
# and then asks user to choose whether to enter equations manually or to enter the file name to read from. 

# The following 3 functions work with user input if manual entry is chosen.
def do_manual_calculations():
    while True:
        num1, num2 = user_input_numbers()
        operation = user_input_operation()
        try:
            calculate(num1, num2, operation)
        except ZeroDivisionError:
            print("Division by zero! Please start again.")
            continue
        result = f"{num1} {operation} {num2} = {calculate(num1, num2, operation)}"
        append_to_file(result)
        print(result)
        exit = input("Do you want to perform another operation? (Yes/No): ")
        if exit.lower() == 'yes':
            continue
        else:
            print("""You have entered \'No\' or something different from \'Yes\', so the calculator stops. To use it again, restart the program. 
Your equations with results were saved to a file called """ + file_to_save)
            break

def user_input_numbers():
    while True:
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            break
        except: 
            print("Seems like you didn't enter numbers or didn't do it in a numerical format. Please try again.")
    return num1, num2

def user_input_operation():
    while True:
        operation = input("""Choose the operation you want to perform: 
        for addition enter +
        for substraction enter - 
        for multiplication enter *
        for devision enter /
        """)
        if operation not in ['+', '-', '*', '/']:
            print("You haven't chosen any of the listed operations. Please start again.")
        else:
            return operation
    

# The following 3 functions refer to the calculations from file. 
# By default: let't assume, that the equations in the file are entered in the following format: num1(space)operation(space)num2
def do_file_calculations():
    while True:    
        equation_file = input("Please enter the name of your equations file: ")
        try: 
            with open(equation_file, 'r') as equation_file:
                line_elements = read_file_from_user(equation_file)
                calculate_line_elements(line_elements)
                print("Calculations are completed. Results are recorded in a file called " + file_to_save)
                break
        except FileNotFoundError:
            print("This file does not exist.")
        except ValueError:
            print("Invalid file format. Equations in file are expected to be in number1(space)operation(space)number2")

def read_file_from_user(equation_file): #distinguish between input file and output file
    line_elements = []
    lines = equation_file.readlines()
    for line in lines:
        parsed_elements = line.strip().split(" ")
        if (len(parsed_elements) != 3):
            raise ValueError
        
        # will throw ValueError if not floats are passed in file
        parsed_elements[0] = float(parsed_elements[0])
        parsed_elements[2] = float(parsed_elements[2])

        line_elements.append(parsed_elements)
    return line_elements
        
def calculate_line_elements(line_elements): 
    with open(file_to_save, 'a') as results_file:
        for element in line_elements:
            try:
                result = f"{element[0]} {element[1]} {element[2]} = {calculate(element[0], element[2], element[1])}"
            except ZeroDivisionError:
                result = "Division by zero is not possible"
            finally:
                print(result)
                results_file.write(result + '\n')

# Functions that define simple operations which calculator performs:
def add(num1, num2): 
    return num1 + num2

def substract(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    return num1 / num2

def calculate(num1, num2, operation):
    match operation: 
        case '+':
            return add(num1, num2)
        case '-':
            return substract(num1, num2)
        case '*':
            return multiply(num1, num2)
        case '/':
            return divide(num1, num2)


# The fuctions that ask user to enter the name of the file for results and save the results into the file of user choice.
def ask_for_file_to_save():
    while True:
        file_to_save = input("Enter the file name in a <name.txt> format in which you want to save the results of your equations: ")
        if file_to_save[-4:] != '.txt':
            print("You haven't entered the file name in a .txt format.")
            continue
        break
    return file_to_save

def append_to_file(result):
    with open(file_to_save, 'a') as results_file:
        results_file.write(result + '\n')
    return results_file

# The main body of the calculator starts here:
print("Welcome to our simple calculator!")
file_to_save = ask_for_file_to_save()
while True:
    user_choice = input("""Do you want to enter calculations manually or calculate the equations from your file? 
    enter M - for manual path or F - for program to read from your file: """)
    if user_choice.lower() == 'm':
        do_manual_calculations()
        break
    elif user_choice.lower() == 'f':
        do_file_calculations()
        break
    else:
        print("You haven't chosen the path. Please try again.")

