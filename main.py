import os
import ratnum_div as rd
import ratnum_int_power_div as rpd
import ratnum_frac_power as rfp
import ratnum_frac_power_div as rfpd

def main():
    os.system("cls")
    # program terminates if login is unsuccessful
    if login():
        exit()

    exit_flag = False
    # looping until menu() returns True
    while exit_flag == False:
        os.system("cls")
        exit_flag = menu()

def menu():
    print("*** Main Menu ***")
    print("1. Fraction division")
    print("2. Fraction to an integer power division")
    print("3. Fraction to a fractional power")
    print("4. Fraction to a fractional power division")
    print("5. End Program")
    print("*" * 17)
    option = input("Enter your option (1-4): ")
    print()

    if option == "1":
        rd.frac_division()
        return False
    elif option == "2":
        rpd.int_power_division()
        return False
    elif option == "3":
        rfp.frac_power()
        return False
    elif option == "4":
        rfpd.frac_power_division()
        return False
    elif option == "5":
        print("Thank you for using this project!")
        return True
    else:
        print("Invalid input. Try again!")
        input("Press Enter to return to main menu...")
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

    # create new user details if username is not in the login dataset
    if check_user not in users:
        print("Username not found. Creating new login information...")
        check_pass = input("Password: ")
        with open("login.txt", "a") as f:
            f.write(f"{check_user}-{check_pass}\n")
        print()
        print("New user created. Login successful!")
        input("Press Enter to go to main menu...")
        return False

    # check if password match the passwrod in the login dataset
    remaining_attempts = 3
    while remaining_attempts > 0:
        check_pass = input(f"Password ({remaining_attempts} attempt(s) left): ")
        print()
        if users[check_user] == check_pass:
            print("Login successful!")
            input("Press Enter to proceed to main menu...")
            return False
        # if it is not at the last attempt
        if remaining_attempts != 1:
            print("Wrong password! Please try again.")
        remaining_attempts -= 1
    print("Wrong password!")
    print("Program ended.")
    return True

main()