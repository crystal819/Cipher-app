ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

ROTORS = {  'I':    ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
            'II':   ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
            'III':  ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
            'IV':   ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
            'V':    ("VZBRGITYUPSDNHLXAWMJQOFECK", "Z")}

def index_to_letter(index):
    index = index % 26
    return ALPHABET[index]

def letter_to_index(letter):
    letter = letter.upper()
    return ord(letter)-65

def plugboard_txt(pairs_txt, enc_let):
    pairs_txt += ' '
    if type(pairs_txt) == str:
        for i in range(len(pairs_txt)):
            if ord(pairs_txt[i].upper()) >= 65 and ord(pairs_txt[i].upper()) < 91:
                if pairs_txt[i] == enc_let.upper():
                    if ord(pairs_txt[i+1].upper()) >= 65 and ord(pairs_txt[i+1].upper()) < 91:
                        enc_let = pairs_txt[i+1]
                    else:
                        enc_let = pairs_txt[i-1]
                    break
    return enc_let


class Rotor:
    def __init__(self, wiring, notch, ring_setting, position):
        self.wiring = wiring.upper()
        self.notch = notch.upper()
        self.inverse_wiring = self._build_inverse()
        self.ring_setting = ring_setting % 26
        self.position = position % 26
    
    def atNotch(self):
        if index_to_letter(self.position) == self.notch:
            return True
        return False
    
    def step(self):
        self.position = (self.position + 1) % 26

    def _build_inverse(self):
        inv = []
        for _ in range(26):
            inv.append('_')
        for i in range(len(self.wiring)):
            inv[letter_to_index(self.wiring[i])] = index_to_letter(i)
        inverse_wiring = ''
        for let in inv:
            inverse_wiring += let
        return inverse_wiring
    
    def set_ring_setting(self, ring):
        if type(ring) == str:
            ring = letter_to_index(ring)
        self.ring_setting = ring % 26

    def set_position(self, letter):
        self.position = letter_to_index(letter)

    def encode_forward(self, enc_let):
        shifted_in = (enc_let + self.position - self.ring_setting) % 26
        wired = letter_to_index(self.wiring[shifted_in])
        out = (wired - self.position + self.ring_setting) % 26
        return out
    
    def encode_backwards(self, enc_let):
        shifted_in = (enc_let + self.position - self.ring_setting) % 26
        wired = letter_to_index(self.inverse_wiring[shifted_in])
        out = (wired - self.position + self.ring_setting) % 26
        return out

class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring.upper()
    
    def reflect(self, index):
        return letter_to_index(self.wiring[index])

class Enigma:
    def __init__(self, pairs_txt, rotors): #left to right, slow to fast rotor order
        self.rotors = rotors
        self.pairs_txt = pairs_txt
        self.reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        

    def step_rotors(self):
        will_step = []
        for i in range(len(self.rotors)):
            will_step.append(False)
        will_step[-1] = True #rightmost rotor will always step

        for i in range(len(self.rotors)):
            if self.rotors[i].atNotch(): #makes rotors
                will_step[i] = True

        for i in range(len(self.rotors)):
            if will_step[i]:
                self.rotors[i].step()
        
    def encrypt_char(self, let):
        if not let.isalpha():
            return let
        self.step_rotors()
        enc_let = letter_to_index(plugboard_txt(self.pairs_txt, let))
        for rotor in reversed(self.rotors):
            enc_let = rotor.encode_forward(enc_let)
        enc_let = self.reflector.reflect(enc_let)
        for rotor in self.rotors:
            enc_let = rotor.encode_backwards(enc_let)
        enc_let = plugboard_txt(self.pairs_txt, index_to_letter(enc_let))
        return enc_let

    def encrypt(self, plain_text):
        cipher_text = ''
        for let in plain_text:
            if not let.isalpha():
                continue
            cipher_text += self.encrypt_char(let).lower()
        return cipher_text
    
        


if __name__ == '__main__':
    '''
    pairs_txt = input("Enter pairs of letters you want to swap: ")
    rotors = []
    n_rotors = int(input("Do you want 3 or 4 rotors: "))
    while len(rotors) < n_rotors:
        rotor = input("Enter what rotor you want to use: ")
        wiring = ROTORS[rotor][0]
        notch = ROTORS[rotor][1]
        ring_setting = int(input("Enter what ring setting you want <int>: "))
        position = letter_to_index(input("Enter what letter you want for the starting position: "))
        rotors.append(Rotor(wiring, notch, ring_setting, position))
    '''
    plugboard_input = ''
    rotor1 = Rotor(ROTORS["I"][0], ROTORS['I'][1], 1, 1)
    rotor2 = Rotor(ROTORS["II"][0], ROTORS['II'][1], 1, 4)
    rotor3 = Rotor(ROTORS["III"][0], ROTORS['III'][1], 1, 21)
    rotors = [rotor1, rotor2, rotor3] #left to right, slow to fast
    plain_text = input("Enter the text you want to encrypt/decrypt: ")
    enigma = Enigma(plugboard_input, rotors)
    cipher_text = enigma.encrypt(plain_text)
    print(cipher_text)