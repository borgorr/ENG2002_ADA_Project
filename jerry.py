import math

class ratNum:
    def __init__(self, a, b, n):
        self.a = int(a)
        self.b = int(b)
        self.n = int(n)

    def __str__(self):
        return f"({self.a}/{self.b})^{self.n}"

def menu():
    print("***Menu***")
    print("1. Division")
    print("2. Exit")
    select = input("Please choose the action (1 for Division, 2 to Exit): ")
    print("**********")
    if select == '1':
        if login():
            division()
            return False
        else:
            return True
    elif select == '2':
        print("Thank you for using this project!")
        return True
    else:
        print("Invalid Input, please enter a valid input and try again (1 or 2).")
        return False

def login():
    # Try to read existing users; if file doesn't exist, start with an empty list
    try:
        with open("login.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    users = {}
    for line in lines:
        line = line.strip()
        if '-' in line:
            username, password = line.split('-', 1)
            users[username] = password

    check_user = input("Username: ")

    if check_user in users:
        attempts = 3
        while attempts > 0:
            check_pass = input(f"Password ({attempts} attempt(s) left): ")
            if users[check_user] == check_pass:
                print("Login successful!")
                return True
            attempts -= 1
            if attempts == 0:
                print("Wrong password!")
                print("Program ended.")
                return False
            else:
                print("Wrong password! Please try again.")
    else:
        print("Username not found. Creating new login information...")
        check_pass = input("Password: ")
        with open("login.txt", "a") as f:
            f.write(f"{check_user}-{check_pass}\n")
        print("New user created. Login successful!")
        return True

def division():
    #apply an integer exponent to a fraction (a/b)^p
    def power_frac(a, b, p):
        if p >= 0:
            return a ** p, b ** p
        else:
            # (a/b)^(-p) = (b/a)^p
            return b ** (-p), a ** (-p)

    # First rational number
    while True:
        data = input("Enter numerator, denominator, power of 1st number (a b n): ").split()
        if len(data) != 3:
            print("Please enter three integers.")
            continue
        n1, d1, p1 = map(int, data)
        if d1 == 0:
            print("ERROR! Denominator must not be zero.")
            continue
        if n1 == 0:
            print("ERROR! Numerator must not be zero (zero base not allowed).")
            continue
        break
    r1 = ratNum(n1, d1, p1)

    # Second rational number
    while True:
        data = input("Enter numerator, denominator, power of 2nd number (a b n): ").split()
        if len(data) != 3:
            print("Please enter three integers.")
            continue
        n2, d2, p2 = map(int, data)
        if d2 == 0:
            print("ERROR! Denominator must not be zero.")
            continue
        if n2 == 0:
            print("ERROR! Numerator must not be zero (zero base not allowed).")
            continue
        break
    r2 = ratNum(n2, d2, p2)

    # Compute each number raised to its power
    num1, den1 = power_frac(r1.a, r1.b, r1.n)
    num2, den2 = power_frac(r2.a, r2.b, r2.n)

    # Perform division: (num1/den1) / (num2/den2) = (num1 * den2) / (den1 * num2)
    result_num = num1 * den2
    result_den = den1 * num2

    # Simplify the resulting fraction
    result_num, result_den = simplify(result_num, result_den)

    # Result is a simple fraction (power 1)
    result = ratNum(result_num, result_den, 1)
    print(f"{r1} / {r2} = {result}")
    
def simplify(a, b):
    gcd = math.gcd(a, b)
    return (a // gcd, b // gcd)

#main
exitflag = False
while not exitflag:
    exitflag = menu()