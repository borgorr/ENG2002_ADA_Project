import math

class ratNum:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    # return string
    def __str__(self):
        return f"({self.a}/{self.b})"

    # simplify the fraction when there are common factors
    # remove negative sign in denominator
    def simplify(self):
        gcd = math.gcd(self.a, self.b)
        if self.b < 0:
            (self.a, self.b) = (-self.a, -self.b)
        return ratNum(self.a // gcd, self.b // gcd)
    
# invalid if fraction is 0 or base is 0
def valid(numerator, denominator):
    if numerator == 0:
        print("ERROR! Numerator must a non-zero integer.")
        return False
    if denominator <= 0:
        print("ERROR! Denominator must be a positive integer.")
        return False
    return True

def frac_division():
    # ask the user for the 1st and 2nd fraction
    for i in range(2):
        print(f"Enter the numerator (a), denominator (b) of your {["1st", "2nd"][i]} fraction (a / b)")
        print("a must be an integer.")
        print("b must be a non-zeroo integer.")
        print("Format: a, b")

        # turn the 2 inputs into 2 integers
        try:
            numer, deno = map(int, input("Enter: ").split(","))
            print()
        except ValueError:
            print()
            print("ERROR! Incorrect format of number.")
            input("Press Enter to return to menu...")
            print()
            return False
        # return to menu if fraction is invalid
        if not valid(numer, deno):
            input("Press Enter to return to menu...")
            print()
            return False
        # store number details into frac1 in the first iteration
        if i == 0:
            frac1 = ratNum(numer, deno)
        # store number details into frac1 in the second iteration
        if i == 1:
            frac2 = ratNum(numer, deno)

    if frac2.a == 0:
        print("ERROR! Divisor must be non-zero.")
        input("Press Enter to return to menu...")
        print()
        return False

    # (n1 / d1) / (n2 / d2) = (n1 * d2) / (n2 * d1)
    result = ratNum(frac1.a * frac2.b, frac2.a * frac1.b).simplify()

    print(f"{frac1} / {frac2} = ({result.a}/{result.b})")
    input("Press Enter to return to menu...")
    print()