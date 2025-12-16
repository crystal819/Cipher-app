import random

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 
          43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 
          101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 
          151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 
          199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 
          263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 
          317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 
          383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 
          443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 
          503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 
          577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 
          641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 
          701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 
          769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 
          839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 
          911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 
          983, 991, 997]

def encrypt(plain_text, public_key):
    parts = public_key.split() #separates a string of 2 numbers separated by a space and then assigns them onto n and e
    n, e = int(parts[0]), int(parts[1])

    if type(plain_text) == str:
        cipher_text = ''
        for let in plain_text:
            cipher_text += str((ord(let)**e) % n) + ' '
    else:        
        cipher_text = (plain_text**e) % n
    return cipher_text[:-1]

def decrypt(cipher_text, private_key):
    parts = private_key.split() #separates a string of 2 numbers separated by a space and then assigns them onto n and d
    n, d = int(parts[0]), int(parts[1])

    if type(cipher_text) == str:
        cipher_text += ' '
        plain_text = ''
        numb = ''
        for num in cipher_text:
            if num != ' ':
                numb += num
                continue
            else:
                plain_text += chr((int(numb)**d) % n)
                numb = ''
    else:
        plain_text = (cipher_text**d) % n
    return plain_text



def generate_primes(upper_limit):
    primes = []
    for i in range(2, upper_limit):
        isprime = True
        for prime in primes:
            if i % prime == 0:
                isprime = False
        if isprime:
            primes.append(i)
    return primes

class Rsa:
    def __init__(self, p = None, q = None, e = None):
        if p == None:
             p = PRIMES[random.randint(1, len(PRIMES))-1]
        if q == None:
            q = PRIMES[random.randint(1, len(PRIMES))-1]
        while p == q:
            q = self.PRIMES[random.randint(1, len(self.PRIMES))-1]

        self.n = p*q
        eulers_totient = (p-1)*(q-1)
        
        if e == None: #allows the user to choose a value for the public exponent
            self.e = random.randint(2, eulers_totient-1)
            while self.find_gcd(self.e, eulers_totient) != 1:
                self.e = random.randint(2, eulers_totient-1)
        else:
            self.e = e
        self.d = 1
        while (self.e*self.d)%eulers_totient != 1:
            self.d += 1
        
        self.public_key = str(self.n) + ' ' + str(self.e)
        self.private_key = str(self.n) + ' ' + str(self.d)

    def sign(self, m):
        signature = (m**self.d) % self.n
        return signature
    
    def find_factors(self, num):
        factors = []
        for i in range(1, num+1):
            if num % i == 0:
                factors.append(i)
        return factors

    def find_gcd(self, num1, num2):
        num1_factors = self.find_factors(num1)
        num2_factors = self.find_factors(num2)
        common_factors = []
        for i in range(len(num1_factors)):
            for j in range(len(num2_factors)):
                if num1_factors[i] == num2_factors[j]:
                    common_factors.append(num1_factors[i])
        gcd = 1
        for num in common_factors:
            if num > gcd:
                gcd = num
        return gcd






if __name__ == '__main__':
    rsa = Rsa(17, 111, 31)
    message = input("Enter your message: ")
    print(encrypt(message, rsa.public_key))
    
