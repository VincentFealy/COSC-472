#COSC 472 Network Security
#Project 2: Cryptography algorithms implementation
#Vincent Fealy
#Must have makefile in project folder
#Type "make run" into the terminal to run script

import os
import string

#Function checks if the input file exists
def check_file_exists(filename):
    return os.path.isfile(filename)

#Function handles non-alphabetic characters 
#returns the non-alphabetic character unchanged
def shift_character(c, shift):
    if c.isalpha():  #checks if the character is an alphabet
        base = ord('A') if c.isupper() else ord('a')
        return chr((ord(c) - base + shift) % 26 + base)
    return c

#Caesar Cipher
def caesar(text, key, encrypt=True):
    shift = ord(key.lower()) - ord('a')  #convert key to shift value
    if not encrypt:
        shift = -shift
    result = ''.join(shift_character(c, shift) for c in text)
    return result

#Monoalphabetic Cipher
def monoalphabetic(text, key, encrypt=True):
    #cipher mapping
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    key = ''.join(sorted(set(key), key=key.index))  #remove dups
    key = key.lower()
    ciphertext_alphabet = key + ''.join([c for c in alphabet if c not in key])

    #swap alphabets for decryption
    if not encrypt:
        mapping = {ciphertext_alphabet[i]: alphabet[i] for i in range(26)}
    else:
        mapping = {alphabet[i]: ciphertext_alphabet[i] for i in range(26)}

    result = []
    for char in text:
        if char.isalpha():
            if char.isupper():
                result.append(mapping[char.lower()].upper())  #Preserve case
            else:
                result.append(mapping[char])
        else:
            result.append(char)  
    return ''.join(result)

#Polyalphabetic Cipher
def polyalphabetic(text, key, encrypt=True):
    result = []
    key_length = len(key)
    shift_direction = 1 if encrypt else -1

    for i, c in enumerate(text):
        if c.isalpha():
            shift = ord(key[i % key_length].lower()) - ord('a')
            result.append(shift_character(c, shift * shift_direction))
        else:
            result.append(c)  #Preserve non-alphabetic characters
    return ''.join(result)

#Toy Tetragraph Hash
def toyTetragraphHash(text):
    text = text.replace(' ', '').upper()
    if len(text) % 4 != 0:
        text += 'X' * (4 - len(text) % 4)  # Padding with 'X'

    hash_value = 0
    for i in range(0, len(text), 4):
        block = text[i:i+4]
        block_value = sum(ord(block[j]) for j in range(4))
        hash_value = (hash_value + block_value) % 10000  # Mod 10000
    return hash_value

#This is my main program
#will prompt user for choices e, q, or d
#then will ask user for file to input
#then asks user for what cipher they want to use
def main():
    while True:
        choice = input("Choose e, d, or q to encrypt, decrypt, or quit: ").lower()
        if choice == 'q':
            break
        #error checking
        if choice not in ['e', 'd']:
            print("Invalid option! Please choose 'e' for encrypt, 'd' for decrypt, or 'q' to quit")
            continue

        filename = input("Enter a filename: ")
        if not check_file_exists(filename):
            print("Error: File not found")
            continue

        #opening the input file
        with open(filename, 'r') as f:
            text = f.read().strip()

        #Checks if the file length exceeds 200 characters
        if len(text) > 200:
            print("Error: File contains more than 200 characters. Please provide a shorter file")
            continue

        cipher_choice = input("Choose cipher: (1) Caesar, (2) Monoalphabetic, (3) Polyalphabetic, (4) TTH: ")
        if cipher_choice not in ['1', '2', '3', '4']:
            print("Invalid choice. Please enter a number between 1 and 4")
            continue

        if cipher_choice == '1':  #Caesar Cipher for 1
            key = input("Enter a single character key for Caesar Cipher: ").lower()
            if len(key) != 1 or not key.isalpha():
                print("Error: Key must be a single alphabetical character (a-z)")
                continue
            result = caesar(text, key, encrypt=(choice == 'e'))

        elif cipher_choice == '2':  #Monoalphabetic Cipher for 2
            key = input("Enter a 6-character key for Monoalphabetic Cipher: ").lower()
            if len(key) != 6 or not key.isalpha():
                print("Error: Key must be exactly 6 alphabetical characters.")
                continue
            result = monoalphabetic(text, key, encrypt=(choice == 'e'))

        elif cipher_choice == '3':  #Polyalphabetic Cipher for 3
            key = input("Enter a 3-character key for Polyalphabetic Cipher: ").lower()
            if len(key) != 3 or not key.isalpha():
                print("Error: Key must be exactly 3 alphabetical characters.")
                continue
            result = polyalphabetic(text, key, encrypt=(choice == 'e'))

        elif cipher_choice == '4':  #TTH for 4
            print("Running Toy Tetragraph Hash")
            result = toyTetragraphHash(text)

        print(f"Result: {result}\n")

if __name__ == "__main__":
    main()  #only runs if the script is executed directly
