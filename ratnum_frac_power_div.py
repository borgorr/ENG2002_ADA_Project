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
        return (self.a < 0 or self.b < 0) and self.n_deno % 2 == 0

    # apply an integer exponent to a fraction (a / b) ^ n
    def remove_expo_numer(self):
        if self.n_deno < 0:
            self.n_numer = -self.n_numer
            self.n_deno = -self.n_deno
        if self.n_numer < 0:
            self.a, self.b = self.b, self.a
            self.n_numer = -self.n_numer
        self.a **= self.n_numer
        self.b **= self.n_numer
        self.n_numer = 1
        return ratNum(self.a, self.b, self.n_numer, self.n_deno)
    
    def remove_expo_deno(self):
        self.a **= 1 / self.n_deno
        self.b **= 1 / self.n_deno
        self.n_deno = 1
        return ratNum(self.a, self.b, self.n_numer, self.n_deno)

    # simplify the fraction when there are common factors
    # remove negative sign in denominator
    def simplify(self):
        gcd = math.gcd(self.a, self.b)
        if self.b < 0:
            (self.a, self.b) = (-self.a, -self.b)
        self.a //= gcd
        self.b //= gcd
        return ratNum(self.a, self.b, self.n_numer, self.n_deno)

class Surd:
    def __init__(self, coeff, index, radicand, complex):
        self.coeff = coeff
        self.index = index
        self.radicand = radicand
        self.complex = complex

    def factor_surd(self):
        # put negative sign at coefficient if root index is odd
        if self.index % 2 == 1 and self.radicand < 0:
            self.coeff, self.radicand = -self.coeff, -self.radicand

        # raise a complex flag if root index is 2 and radicand is 0
        elif self.index == 2 and self.radicand < 0:
            self.complex = True
            self.radicand = -self.radicand
        
        elif self.index % 2 == 0 and self.radicand < 0:
            print("ERROR! Result contains even order of root larger than 2 with negative radicand.")
            input("Press Enter to return to menu...")
            print()
            return False
        
        # consider root index (n), radicand (a) n√(a)
        # maximum possible root factor must be smaller than or equal to n√(a) rounded up
        max_root_factor = math.ceil(self.radicand ** (1 / self.index))

        # iterate from the maximum possible root factor to 1 to find the greatest root factor
        # then factor the greatest root factor out of the surd
        for i in range(max_root_factor, 0, -1):
            if (self.radicand / (i ** self.index)).is_integer():
                new_coeff = i
                new_radicand = self.radicand // i ** self.index
                break
        self.coeff *= new_coeff
        if self.radicand == 1:
            self.index = 1
        return Surd(self.coeff, self.index, new_radicand, self.complex)

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
            input("Press Enter to return to menu...")
            print()
            return False
        # return to menu if fraction is invalid
        if not (valid(numer, deno) or valid(expo_numer, expo_deno)):
            input("Press Enter to return to menu...")
            print()
            return False
        # store number details into frac1 in the first iteration
        if i == 0:
            frac1 = ratNum(numer, deno, expo_numer, expo_deno)
        # store number details into frac1 in the second iteration
        if i == 1:
            frac2 = ratNum(numer, deno, expo_numer, expo_deno)
    
    # result = 1 if value of the 1st and 2nd value are the same
    if (frac1.a / frac1.b) ** (frac1.n_numer / frac1.n_deno) == (frac2.a / frac2.b) ** (frac2.n_numer / frac2.n_deno):
        print(f"{frac1} / {frac2} = 1")
        input("Press Enter to return to menu...")
        print()
        return False

    # simplify the fraction by removing the exponent
    new_frac1 = frac1.remove_expo_numer()
    new_frac2 = frac2.remove_expo_numer()

    new_frac1 = ratNum(Surd(1, frac1.n_deno, frac1.a, False).factor_surd(), Surd(1, frac1.n_deno, frac1.b, False).factor_surd(), 1, 1)
    new_frac2 = ratNum(Surd(1, frac2.n_deno, frac2.a, False).factor_surd(), Surd(1, frac2.n_deno, frac2.b, False).factor_surd(), 1, 1)
    
    # simplify surd part
    if new_frac1.a.surd_part() == new_frac1.b.surd_part():
        new_frac1.a.index, new_frac1.a.radicand, new_frac1.b.index, new_frac1.b.radicand = 1, 1, 1, 1
    if new_frac2.a.surd_part() == new_frac2.b.surd_part():
        new_frac2.a.index, new_frac2.a.radicand, new_frac2.b.index, new_frac2.b.radicand = 1, 1, 1, 1
    if new_frac1.a.surd_part() == new_frac2.a.surd_part():
        new_frac1.a.index, new_frac1.a.radicand, new_frac2.a.index, new_frac2.a.radicand = 1, 1, 1, 1
    if new_frac1.b.surd_part() == new_frac2.b.surd_part():
        new_frac1.b.index, new_frac1.b.radicand, new_frac2.b.index, new_frac2.b.radicand = 1, 1, 1, 1

    # simplify imaginary part
    if new_frac1.a.complex and new_frac1.b.complex:
        new_frac1.a.complex, new_frac1.b.complex = False, False
    if new_frac2.a.complex and new_frac2.b.complex:
        new_frac2.a.complex, new_frac2.b.complex = False, False
    if new_frac1.a.complex and new_frac2.a.complex:
        new_frac1.a.complex, new_frac2.a.complex = False, False
    if new_frac1.b.complex and new_frac2.b.complex:
        new_frac1.b.complex, new_frac2.b.complex = False, False

    # rationalise square roots
    if new_frac1.a.index == 2 and new_frac2.b.index == 2 and new_frac1.a.radicand == new_frac2.b.radicand:
        new_frac1.a.coeff = new_frac1.a.radicand
        new_frac1.a.radicand, new_frac2.b.radicand = 1, 1
    if new_frac2.a.index == 2 and new_frac1.b.index == 2 and new_frac2.a.radicand == new_frac1.b.radicand:
        new_frac2.a.coeff = new_frac2.a.radicand
        new_frac2.a.radicand, new_frac1.b.radicand = 1, 1

    # i * i = -1
    if new_frac1.a.complex and new_frac2.b.complex:
        new_frac1.a.coeff, new_frac1.a.complex, new_frac2.b.complex = -new_frac1.a.coeff, False, False
    if new_frac2.a.complex and new_frac1.b.complex:
        new_frac2.a.coeff, new_frac2.a.complex, new_frac1.b.complex = -new_frac2.a.coeff, False, False
    
    if new_frac1.a.complex or new_frac1.b.complex or new_frac2.a.complex or new_frac2.b.complex:
        print("ERROR! Result contains imaginary number.")
        input("Press Enter to return to menu...")
        print()
        return False
    
    if new_frac1.a.radicand != 1 or new_frac1.b.radicand != 1 or new_frac2.a.radicand != 1 or new_frac2.b.radicand != 1:
        print("ERROR! Result contains irrational number.")
        input("Press Enter to return to menu...")
        print()
        return False

    result = ratNum(new_frac1.a.coeff * new_frac2.b.coeff, new_frac2.a.coeff * new_frac1.b.coeff , 1, 1).simplify()
    print(f"{frac1} / {frac2} = ({result.a}/{result.b})")
    input("Press Enter to return to menu...")
    print()
    return False
    
frac_power_division()