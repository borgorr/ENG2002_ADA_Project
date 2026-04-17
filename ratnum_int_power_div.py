import math

class ratNum:
    def __init__(self, a, b, n):
        self.a = a
        self.b = b
        self.n = n

    # return string
    def __str__(self):
        if self.n == 1:
            return f"({self.a}/{self.b})"
        return f"({self.a}/{self.b}) ^ ({self.n})"

    # apply an integer exponent to a fraction (a / b) ^ n
    def remove_expo(self):
        if self.n < 0:
            self.a, self.b = self.b, self.a
            self.n *= -1
        self.a **= self.n
        self.b **= self.n
        self.n = 1
        return ratNum(self.a, self.b, self.n)
    
    # simplify the fraction when there are common factors
    # remove negative sign in denominator
    def simplify(self):
        gcd = math.gcd(self.a, self.b)
        self.a //= gcd
        self.b //= gcd
        return ratNum(self.a, self.b, self.n)
    
# invalid if fraction is 0 or base is 0
def valid(numerator, denominator):
    if numerator == 0:
        print("ERROR! Numerator must a non-zero integer.")
        return False
    if denominator <= 0:
        print("ERROR! Denominator must be a positive integer.")
        return False
    return True

def int_power_division():
    # ask the user for the 1st and 2nd fraction
    for i in range(2):
        print(f"Enter the numerator (a), denominator (b), exponent (n) of your {['1st', '2nd'][i]} fraction (a / b) ^ (n).")
        print("a, b must be non-zero integers.")
        print("n must be an integer.")
        print("Format: a, b, n")
        # turn the 4 inputs into 4 integers
        try:
            numer, deno, expo = map(int, input("Enter: ").split(","))
            print()
        except ValueError:
            print()
            print("ERROR! Incorrect format of number.")
            input("Press Enter to return to main menu...")
            print()
            return False
        # return to menu if fraction is invalid
        if not valid(numer, deno):
            input("Press Enter to return to main menu...")
            print()
            return False
        # store number details into frac1 in the first iteration
        if i == 0:
            frac1 = ratNum(numer, deno, expo)
        # store number details into frac1 in the second iteration
        if i == 1:
            frac2 = ratNum(numer, deno, expo)

    # simplify the fraction by removing the exponent
    sim_frac1 = frac1.remove_expo()
    sim_frac2 = frac2.remove_expo()

    # (n1 / d1) / (n2 / d2) = (n1 * d2) / (n2 * d1)
    result = ratNum(sim_frac1.a * sim_frac2.b, sim_frac2.a * sim_frac1.b, 1).simplify()

    print(f"{frac1} / {frac2} = ({result.a}/{result.b})")
    input("Press Enter to return to main menu...")
    print()