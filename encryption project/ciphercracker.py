import caesarcipher

def calc_freq(input_text):
    let_freq = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for let in input_text:
        index = ord(let.upper())-65
        if index >= 0 and index <= 26:
            let_freq[index] += 1
    return let_freq


def index_of_coincidence(cipher_text):
    letter_freq = calc_freq(cipher_text)
    numerator = 0
    total  = 0
    for letter in letter_freq:
        if letter == 0:
            continue
        numerator += letter*(letter-1)
        total += letter
    IoC = numerator / (total*(total-1))
    return IoC

def crack_caesar(cipher_text): #caesar crack
    let_freq = calc_freq(cipher_text)
    top_3_let_freq_index = []
    highest = 0
    highest_index = 0
    for j in range(3):
        for i in range(26):
            if (let_freq[i] > highest) and (i not in top_3_let_freq_index):
                highest = let_freq[i]
                highest_index = i
        top_3_let_freq_index.append(highest_index)
        highest = 0
        highest_index = 0

    top_3_cracked = []
    for i in range(3):
        key = top_3_let_freq_index[i] - 4 #index of the 3 most occuring letters in the cipher text compared to the index of the letter e since its the most common in english
        if key < 0:
            key += 26
        top_3_cracked.append((caesarcipher.decrypt(cipher_text, key), key))

    return top_3_cracked
    





if __name__ == '__main__':
    print(crack_caesar('olssvtfuhtlpzahyhzhukphtaolnylhalzajyfwavnyhwolylclyavlepzadpaotbsapwslpuuvchapvuzzbjohzaopzjbyyluahwwspjhapvufvbhylbzpun', calc_freq('olssvtfuhtlpzahyhzhukphtaolnylhalzajyfwavnyhwolylclyavlepzadpaotbsapwslpuuvchapvuzzbjohzaopzjbyyluahwwspjhapvufvbhylbzpun')))