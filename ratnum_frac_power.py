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
    
    def no_principle_value(self):
        return (self.a / self.b) < 0 and self.n_deno % 2 == 0
    
    # apply an integer exponent to a fraction (a / b) ^ (c / d) = (a ^ c / b ^ c) ^ (1 / d)
    def remove_expo_numer(self):
        if self.n_numer < 0:
            self.a, self.b = self.b, self.a
            self.n_numer *= -1
        self.a **= self.n_numer
        self.b **= self.n_numer
        self.n_numer = 1
        return ratNum(self.a, self.b, self.n_numer, self.n_deno)
    
    # simplify the fraction when there are common factors
    # remove negative sign in denominator
    def simplify(self):
        gcd = math.gcd(self.a, self.b)
        self.a //= gcd
        self.b //= gcd
        return ratNum(self.a, self.b, self.n_numer, self.n_deno)

class Surd:
    def __init__(self, coeff, index, radicand):
        self.coeff = coeff
        self.index = index
        self.radicand = radicand
    
    def simplify_surd(self):
        if self.radicand < 0:
            self.coeff *= -1
            self.radicand *= -1
        return Surd(self.coeff, self.index, self.radicand)
    
    def factor_surd(self, factor):
        # consider root index (n), radicand (a) n√(a)
        # maximum possible root factor must be smaller than or equal to n√(a) rounded up
        max_root_factor = math.ceil(self.radicand ** (1 / self.index))
        for i in range(factor, max_root_factor + 1):
            if self.radicand % i ** self.index == 0:
                self.coeff *= i
                self.radicand //= i ** self.index
                return Surd(self.coeff, self.index, self.radicand).factor_surd(i)
        return Surd(self.coeff, self.index, self.radicand)
    
    def surd_part(self):
        return self.index, self.radicand

# invalid if fraction is 0 or base is 0
def valid(numerator, denominator):
    if numerator == 0:
        print("ERROR! Numerator must a non-zero integer.")
        return False
    if denominator <= 0:
        print("ERROR! Denominator must be a positive integer.")
        return False
    return True

def frac_power():
    # ask the user for content of the fraction to a fraction power
    print(f"Enter the numerator (a), denominator (b), numerator of exponent (c), denominator of exponent (d) of your fraction (a / b) ^ (c / d).")
    print("a, b, c, d must be non-zero integers.")
    print("Format: a, b, c, d")
    # turn the 4 inputs into 4 integers
    try:
        numer, deno, expo_numer, expo_deno = map(int, input("Enter: ").split(","))
        print()
    except ValueError:
        print()
        print("ERROR! Incorrect format of number.")
        input("Press Enter to return to main menu...")
        print()
        return False
    # return to menu if fraction is invalid
    if not (valid(numer, deno) and valid(expo_numer, expo_deno)):
        input("Press Enter to return to main menu...")
        print()
        return False
    # store number details into frac
    frac = ratNum(numer, deno, expo_numer, expo_deno)

    # simplify the exponent fraction
    expo = ratNum(frac.n_numer, frac.n_deno, 1, 1).simplify()
    new_frac = ratNum(frac.a, frac.b, expo.a, expo.b)

    # end the function if the result contains no real principle value
    if new_frac.no_principle_value():
        print("Result contains multivalued complex numbers only.")
        input("Press Enter to return to main menu...")
        print()
        return False
    # simplify the fraction by removing the exponent
    new_frac = new_frac.remove_expo_numer()
    new_frac = ratNum(Surd(1, new_frac.n_deno, new_frac.a).simplify_surd().factor_surd(factor=2), Surd(1, new_frac.n_deno, new_frac.b).simplify_surd().factor_surd(factor=2), 1, 1)
    
    # simplify surd part
    if new_frac.a.surd_part() == new_frac.b.surd_part():
        new_frac.a.index = new_frac.a.radicand = new_frac.b.index = new_frac.b.radicand = 1

    if not (new_frac.a.radicand == new_frac.b.radicand == 1):
        print("ERROR! Result contains irrational number.")
        input("Press Enter to return to main menu...")
        print()
        return False

    result = ratNum(new_frac.a.coeff, new_frac.b.coeff, 1, 1).simplify()
    print(f"{frac} = ({result.a}/{result.b})")
    input("Press Enter to return to main menu...")
    print()
    return False