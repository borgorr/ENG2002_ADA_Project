import math

class ratNum:
    def __init__(self, a, b, n_numer, n_deno):
        self.a = a
        self.b = b
        self.n_numer = n_numer
        self.n_deno = n_deno

    # return string
    def __str__(self, original=False):
        # return a original fraction with no extra brackets for the original fraction
        if original:
            return f"({self.a}/{self.b}) ^ ({self.n_numer}/{self.n_deno})" 
        if self.b == 1:
            return f"({self.a})"
        if self.n_numer == 1:
            return f"[({self.a})/({self.b})]"
        if self.n_deno == 1:
            return f"({self.a}/{self.b}) ^ ({self.n_numer})"
        return f"[({self.a})/({self.b})] ^ ({self.n_numer}/{self.n_deno})"
    
    def is_complex(self):
        return (self.a < 0 or self.b < 0) and self.n_deno % 2 == 0

    def is_irrational(self):
        return not ((self.a ** (1 / self.n_deno) % 1).is_integer() and (self.b ** (1 / self.n_deno) % 1).is_integer())
    
    # apply an integer exponent to a fraction (a / b) ^ n
    def remove_power_numer(self):
        if self.n_numer < 0:
            self.a, self.b = self.b, self.a
            self.n_numer = -self.n_numer
        self.a **= self.n_numer
        self.b **= self.n_numer
        self.n_numer = 1
        return ratNum(self.a, self.b, self.n_numer, self.n_deno)
    
    def remove_power_deno(self):
        self.a **= 1 / self.n_deno
        self.b **= 1 / self.n_deno
        self.n_deno = 1
        return ratNum(self.a ** 1 / self.n_deno, self.b ** 1 / self.n_deno, 1)

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
    def __init__(self, coeff, index, radicand):
        self.coeff = coeff
        self.index = index
        self.radicand = radicand

    def __str__(self):
        # omit displaying root part if radicand is 1
        if self.radicand == 1:
            return f"{self.coeff}"
        # omit displaying root index if root index is 2
        if self.index == 2:
            return f"{self.coeff}*√{self.radicand}"
        # coeff * index √ radicand
        return f"{self.coeff}*{self.index}√{self.radicand}"

    def factor_surd(self):
        new_coeff = self.coeff
        new_radicand = self.radicand

        # consider root index (n), radicand (a) n√(a)
        # maximum possible root factor must be smaller than or equal to n√(a) rounded up
        max_root_factor = math.ceil(self.radicand ** (1 / self.index))

        # iterate from the maximum possible root factor to 2 to find the greatest root factor
        # then factor the greatest root factor out of the surd
        for i in range(max_root_factor, 1, -1):
            if (self.radicand / (i ** self.index)).is_integer():
                new_coeff = i
                new_radicand = self.radicand // i ** self.index
                break
        if self.radicand == 1:
            self.index = 1
        return Surd(self.coeff * new_coeff, self.index, new_radicand)

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

    # simplify the fraction by removing the power
    new_frac1 = frac1.remove_power_numer()
    new_frac2 = frac2.remove_power_numer()

    # end the program if complex number is involved
    if new_frac1.is_complex() or new_frac2.is_complex():
        print("ERROR! Complex number involved in calculation.")
        input("Press Enter to return to menu...")
        print()
        return False

    # use Surd class object if the irrational numbers are involved
    elif new_frac1.is_irrational() or new_frac2.is_irrational():
        # print("ERROR! Complex number involved in calculation.")
        # input("Press Enter to return to menu...")
        # print()
        # return False        

        new_frac1_a = Surd(1, frac1.n_deno, frac1.a).factor_surd()
        new_frac1_b = Surd(1, frac1.n_deno, frac1.b).factor_surd()
        new_frac2_a = Surd(1, frac2.n_deno, frac2.a).factor_surd()
        new_frac2_b = Surd(1, frac2.n_deno, frac2.b).factor_surd()

        new_frac1 = ratNum(new_frac1_a, new_frac1_b, 1, 1)
        new_frac2 = ratNum(new_frac2_a, new_frac2_b, 1, 1)

        print(new_frac1)

        result = 0
        # result = ratNum().simplify()


        print(f"{new_frac1, new_frac2}")
        
    else:
        sim_frac1 = sim_frac1.remove_power_deno()
        sim_frac2 = sim_frac2.remove_power_deno()

        # (n1 / d1) / (n2 / d2) = (n1 * d2) / (n2 * d1)
        result = ratNum(sim_frac1.a * sim_frac2.b, sim_frac2.a * sim_frac1.b, 1, 1).simplify()
        
        print(f"{frac1} / {frac2} = ({result.a}/{result.b})")
    input("Press Enter to return to menu...")
    print()