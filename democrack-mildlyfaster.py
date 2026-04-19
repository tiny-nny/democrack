# WARNING
# THIS IS FOR EDUCATIONAL PURPOSES ONLY
# I AM NOT RESPONSIBLE FOR HOW YOU USE THIS
# ver 2.0
# added password input option
# im warning you, dont delete random shit

import itertools
import sys
import string
import random

# -----------------------------
# ASCII BANNER
# -----------------------------
print(r"""
     _                                          _    _ 
  __| | ___ _ __ ___   ___   ___ _ __ __ _  ___| | _| |
 / _` |/ _ \ '_ ` _ \ / _ \ / __| '__/ _` |/ __| |/ / |
| (_| |  __/ | | | | | (_) | (__| | | (_| | (__|   <|_|
 \__,_|\___|_| |_| |_|\___/ \___|_|  \__,_|\___|_|\_(_)
""")

# -----------------------------
# CONFIG
# -----------------------------
CHARACTERS = string.ascii_letters
MIN_LENGTH = 1
MAX_LENGTH = 10
PROGRESS_INTERVAL = 10_000_000

symbols1 = "!@#$%^&*()."
genCHARACTER = string.ascii_letters + string.digits + symbols1

# -----------------------------
# -. Generate password function.
# -----------------------------
def genpasschoose():
    print("\nOptions:\n1 - Generate fully randomized password\n2 - Generate good but memorizable password")
    choice = input("Enter 1 or 2: ")
    if choice == "1":
        genpassran()
    elif choice == "2":
        genpassrem()
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

# generate random password function
def genpassran():
    word = ''.join(random.choice(genCHARACTER) for _ in range(15))
    print(word)

# generate memorable password function
def genpassrem():
    # Read your word list (each word is a line)
    with open("commons.txt", "r") as f:
        words = [line.strip() for line in f]

    # Pick 2 random words
    word1 = random.choice(words).capitalize()
    word2 = random.choice(words).capitalize()

    # Add 2 random digits/symbols using your existing symbols1
    suffix = ''.join(random.choice(symbols1 + string.digits) for _ in range(2))

    # Combine into a password
    password = word1 + word2 + suffix

    print(password)

# -----------------------------
# 0. Choose password source
# -----------------------------
print("Choose password source:")
print("1 - Use pass.txt")
print("2 - Type password manually")
print("3 - Generate Password")

choice = input("Enter 1, 2, or 3: ").strip()

if choice == "1":
    try:
        with open('pass.txt', 'r') as file:
            actual_password = file.readline().strip()
            actual_tuple = tuple(actual_password)
    except FileNotFoundError:
        print("ERROR: You chose pass.txt but it DOES NOT EXIST. Is it in the same folder?")
        print("Load the file or choose option 2 next time.")
        sys.exit(1)

elif choice == "2":
    actual_password = input("Type the password to brute-force: ").strip()
    actual_tuple = tuple(actual_password)

elif choice == "3":
    genpasschoose()
    sys.exit(0)

else:
    print("Invalid choice. Exiting.")
    sys.exit(1)

print("Starting by trying common passes...")

# -----------------------------
# 1. Check common passwords first
# -----------------------------
try:
    with open('commons.txt', 'r') as commons:
        for line in commons:
            guess = line.strip()
            if guess == actual_password:
                print(f"Got it from commons! Password is: {guess}")
                print("Took less than 10k tries! (based on commons size)")
                sys.exit(0)

except FileNotFoundError:
    print("commons.txt not found, skipping common password check. maybe it isn't in the same folder?")

# -----------------------------
# 2. Brute-force
# -----------------------------
print("Wasn't in common passes we had...")
print("Starting brute forcing...")

found = False

# Local variable speed boost
chars = CHARACTERS
product = itertools.product
actual = actual_tuple

for length in range(MIN_LENGTH, MAX_LENGTH + 1):
    for guess in product(chars, repeat=length):

        # Direct tuple comparison (no string creation)
        if guess == actual:
            print(f"Got it! Password is: {''.join(guess)}")
            print("Took probably a few tries! (we dont track amount here)")
            found = True
            break

    if found:
        break

if not found:
    print("\nPassword was not found in the brute-force search space.")
    print("Maybe it's too long, contains numbers, symbols, or uses unsupported characters.")
    print("Perhaps read the instructions next time?")
