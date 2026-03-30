import math

class ratNum:
    def __init__(self, a, b, n):
        self.a = a
        self.b = b
        self.n = n

    # return string
    def __str__(self):
        return(f"({self.a} / {self.b}) ^ ({self.n})")

    # apply an integer exponent to a fraction (a / b) ^ n
    def remove_power(self):
        # (a / b) ^ n = (a ^ n / n ^ n)
        if self.n >= 0:
            return ratNum(self.a ** self.n, self.b ** self.n, 1)
        # (a / b) ^ (-n) = (b ^ n / a ^ n)
        else:
            return ratNum(self.b ** -self.n, self.a ** -self.n, 1)

    # simplify the fraction when there are common factors
    # remove negative sign in denominator
    def simplify(self):
        gcd = math.gcd(self.a, self.b)
        if self.b < 0:
            (self.a, self.b) = (-self.a, -self.b)
        return ratNum(self.a // gcd, self.b // gcd, 1)


# invalid if fraction is 0 or base is 0
def valid(numerator, denominator):
    if numerator == 0:
        print("ERROR! Numerator must not be zero.")
        return False
    if denominator == 0:
        print("ERROR! Denominator must not be zero (zero base is not allowed).")
        return False
    return True

def division():
    # ask the user for the 1st and 2nd fraction
    for i in range(2):
        print(f"Enter the numerator (a), denominator (b), power (n) of your {["1st", "2nd"][i]} number (a / b) ^ (n).")
        print("a, b, n must be integers.")
        print("Format: a, b, n")
        try:
            numer, deno, power = map(int, input("Enter: ").split(","))
            print()
        except ValueError:
            print()
            print("ERROR! Incorrect format of number.")
            print("Returned to menu.")
            return False
        # return to menu if fraction is invalid
        if not valid(numer, deno):
            print("Returned to menu.")
            return False
        # store number details into frac1 in the first iteration
        if i == 0:
            frac1 = ratNum(numer, deno, power)
        # store number details into frac1 in the second iteration
        if i == 1:
            frac2 = ratNum(numer, deno, power)

    # simplify the fraction by removing the power
    sim_frac1 = frac1.remove_power()
    sim_frac2 = frac2.remove_power()

    # (n1 / d1) / (n2 / d2) = (n1 * d2) / (n2 * d1)
    result = ratNum(sim_frac1.a * sim_frac2.b, sim_frac2.a * sim_frac1.b, 1).simplify()

    print(f"{frac1} / {frac2} = ({result.a} / {result.b})")
    input("Press Enter to return to menu...")
    print()