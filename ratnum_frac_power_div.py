import math

class ratNum:
    def __init__(self, a, b, n_numer, n_deno):
        self.a = a
        self.b = b
        self.n_numer = n_numer
        self.n_deno = n_deno

    # return string
    def __str__(self):
        return f"[({self.a}/{self.b}) ^ ({self.n_numer}/{self.n_deno})]"
    
    def is_complex(self):
        return (self.a / self.b) < 0 and self.n_deno > 1
    
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

def frac_power_division():
    # ask the user for the 1st and 2nd fraction
    for i in range(2):
        print(f"Enter the numerator (a), denominator (b), numerator of exponent (c), denominator of exponent (d) of your {["1st", "2nd"][i]} fraction (a / b) ^ (c / d).")
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
        # store number details into frac1 in the first iteration
        if i == 0:
            frac1 = ratNum(numer, deno, expo_numer, expo_deno)
        # store number details into frac1 in the second iteration
        if i == 1:
            frac2 = ratNum(numer, deno, expo_numer, expo_deno)

    # simplify the exponent fraction
    frac1_expo, frac2_expo = ratNum(frac1.n_numer, frac1.n_deno, 1, 1).simplify(), ratNum(frac2.n_numer, frac2.n_deno, 1, 1).simplify()
    new_frac1, new_frac2 = ratNum(frac1.a, frac1.b, frac1_expo.a, frac1_expo.b), ratNum(frac2.a, frac2.b, frac2_expo.a, frac2_expo.b)

    # end the function if the result contains negative number of even roots larger than 2
    if new_frac1.is_complex() or new_frac2.is_complex():
        print("ERROR! Result contains multivalued complex numbers.")
        input("Press Enter to return to main menu...")
        print()
        return False
    # simplify the fraction by removing the exponent
    new_frac1 = new_frac1.remove_expo_numer()
    new_frac2 = new_frac2.remove_expo_numer()

    new_frac1 = ratNum(Surd(1, new_frac1.n_deno, new_frac1.a).factor_surd(factor=2), Surd(1, new_frac1.n_deno, new_frac1.b).factor_surd(factor=2), 1, 1)
    new_frac2 = ratNum(Surd(1, new_frac2.n_deno, new_frac2.a).factor_surd(factor=2), Surd(1, new_frac2.n_deno, new_frac2.b).factor_surd(factor=2), 1, 1)
    
    for top, bottom in [[new_frac1.a, new_frac1.b],
                        [new_frac2.a, new_frac2.b],
                        [new_frac1.a, new_frac2.a],
                        [new_frac1.b, new_frac2.b]]:
        # simplify surd part
        if top.surd_part() == bottom.surd_part():
            top.index = top.radicand = bottom.index = bottom.radicand = 1

    for left, right in [[new_frac1.a, new_frac2.b],
                        [new_frac1.b, new_frac2.a]]:
        # rationalise square roots
        if left.index == right.index == 2 and left.radicand == right.radicand:
            left.coeff = left.radicand
            left.index = left.radicand = right.index = right.radicand = 1
    
    if not (new_frac1.a.radicand == new_frac1.b.radicand == new_frac2.a.radicand == new_frac2.b.radicand == 1):
        print("ERROR! Result contains irrational number.")
        input("Press Enter to return to main menu...")
        print()
        return False

    result = ratNum(new_frac1.a.coeff * new_frac2.b.coeff, new_frac2.a.coeff * new_frac1.b.coeff , 1, 1).simplify()
    print(f"{frac1} / {frac2} = ({result.a}/{result.b})")
    input("Press Enter to return to main menu...")
    print()
    return False