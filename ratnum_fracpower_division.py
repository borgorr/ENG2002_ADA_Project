import math

class ratNum:
    def __init__(self, a, b, n_numer, n_deno):
        self.a = a
        self.b = b
        self.n_numer = n_numer
        self.n_deno = n_deno

    # return string
    def __str__(self):
        return f"({self.a}/{self.b}) ^ ({self.n_numer}/{self.n_deno})"

    def is_irrational(self):
        return not ((self.a ** (1 / self.n_deno) % 1).is_integer() and (self.b ** (1 / self.n_deno) % 1).is_integer())
    
    # apply an integer exponent to a fraction (a / b) ^ n
    def remove_power_numer(self):
        if self.n_numer < 0:
            self.a, self.b = self.b, self.a
            self.n_numer = -self.n_numer
        return ratNum(self.a ** self.n_numer, self.b ** self.n_numer, 1, self.n_deno)
    
    def remove_power_deno(self):
        self.a **= 1 / self.n_deno
        self.b **= 1 / self.n_deno
        return ratNum(self.a ** self.n_numer, self.b ** self.n_numer, 1, self.n_deno)

    # simplify the fraction when there are common factors
    # remove negative sign in denominator
    def simplify(self):
        gcd = math.gcd(self.a, self.b)
        if self.b < 0:
            (self.a, self.b) = (-self.a, -self.b)
        return ratNum(self.a // gcd, self.b // gcd, 1, 1)
    
class Surd:
    def __init__(self, coeff, index, radicand):
        self.coeff = coeff
        self.index = index
        self.radicand = radicand
    
    def __str__(self):
        if self.radicand == 1:
            return f"{self.coeff}"
        if self.index == 2:
            return f"{self.coeff}*√{self.radicand}"
        return f"{self.coeff}*{self.index}√{self.radicand}"

# invalid if fraction is 0 or base is 0
def valid(numerator, denominator):
    if numerator == 0:
        print("ERROR! Numerator must a non zero integer.")
        return False
    if denominator <= 0:
        print("ERROR! Denominator must be a positive integer.")
        return False
    return True

def division_frac_power():
    # ask the user for the 1st and 2nd fraction
    for i in range(2):
        print(f"Enter the numerator (a), denominator (b), power (n) of your {["1st", "2nd"][i]} number (a / b) ^ (c / d).")
        print("a, b, c, d must be integers.")
        print("Format: a, b, c, d")
        # turn the 4 inputs into 4 integers
        try:
            numer, deno, power_numer, power_deno = map(int, input("Enter: ").split(","))
            print()
        except ValueError:
            print()
            print("ERROR! Incorrect format of number.")
            print("Returned to menu.")
            return False
        # return to menu if fraction is invalid
        if not (valid(numer, deno) or valid(power_numer, power_deno)):
            print("Returned to menu.")
            return False
        # store number details into frac1 in the first iteration
        if i == 0:
            frac1 = ratNum(numer, deno, power_numer, power_deno)
        # store number details into frac1 in the second iteration
        if i == 1:
            frac2 = ratNum(numer, deno, power_numer, power_deno)

    # simplify the fraction by removing the power
    sim_frac1 = frac1.remove_power_numer()
    sim_frac2 = frac2.remove_power_numer()

    # if the 
    if sim_frac1.is_irrational() or sim_frac2.is_irrational():
        frac1_a_surd = Surd()
    sim_frac1 = sim_frac1.remove_power_deno()
    sim_frac2 = sim_frac2.remove_power_deno()

    print(f"{sim_frac1, sim_frac2 = }")
    # (n1 / d1) / (n2 / d2) = (n1 * d2) / (n2 * d1)
    result = ratNum(sim_frac1.a * sim_frac2.b, sim_frac2.a * sim_frac1.b, 1, 1).simplify()

    print(f"{frac1} / {frac2} = ({result.a}/{result.b})")
    input("Press Enter to return to menu...")
    print()