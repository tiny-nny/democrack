# WARNING
# THIS IS FOR EDUCATIONAL PURPOSES ONLY
# I AM NOT RESPONSIBLE FOR HOW YOU USE THIS

# ver 2.0
# commented file
# im warning you, dont delete random shit

# itertools is used for generating combinations
import itertools
# sys is used for exiting the program early
import sys
# string gives access to built-in character sets
import string
# lets generator get random shii
import random

# -----------------------------
# ASCII BANNER (NEW IN 1.2)
# -----------------------------
# Displays cool banner at program start.
# Purely cosmetic. Does nothing functional.
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
# You can change this to ascii_lowercase or ascii_uppercase if you want to make it only brute force uppercase or lowercase
CHARACTERS = string.ascii_letters
# change min or max length to however you want, to make min or max length of brute force/search space
MIN_LENGTH = 1
MAX_LENGTH = 10
# the number in between which attempts it will give a progress update
# like "Tried 20000000 times..."
PROGRESS_INTERVAL = 10_000_000
# get the genCHARACTER thing ready for when it generates a password, if it does :)
symbols1 = "!@#$%^&*()."
genCHARACTER = string.ascii_letters + string.digits + symbols1

amtnotit = 0

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
# 0. Choose password source (NEW IN 1.2)
# -----------------------------
# Instead of ALWAYS requiring pass.txt,
# user can now choose between:
# 1) reading pass.txt
# 2) typing password manually

print("Choose password source:")
print("1 - Use pass.txt")
print("2 - Type password manually")
print("3 - Generate Password")

choice = input("Enter 1, 2, or 3: ").strip()

# If option 1 is selected, behave like old version
if choice == "1":

    # Reads password from txt, only first line because i left instructions there too :)
    try:
        with open('pass.txt', 'r') as file:
            actual_password = file.readline().strip()
            actual_tuple = tuple(actual_password)  # Convert once for faster comparison

    # error if pass.txt was not found (bad!!!)
    except FileNotFoundError:
        print("ERROR: You chose pass.txt but it DOES NOT EXIST. Maybe its in a different foldler?.")
        print("(Maybe you dont have it loaded, or you are on an online compiler that doesnt let you import it)")
        sys.exit(1)

# If option 2 is selected, user manually inputs password
elif choice == "2":

    # NEW: does NOT require pass.txt anymore
    actual_password = input("Type the password to brute-force: ").strip()
    # Convert once for faster comparison
    actual_tuple = tuple(actual_password)

elif choice == "3":
    genpasschoose()
    sys.exit(0)

# Anything else = invalid
else:
    print("Invalid choice. Exiting.")
    sys.exit(1)

# IMPORTANT:
# We only print this AFTER password source is selected.
# (1.2 change — no premature printing)
print("Starting by trying common passes...")

# -----------------------------
# 1. Check common passwords first
# -----------------------------
try:
    # opens and tries common passes before brute forcing, to avoid unnecessary work
    with open('commons.txt', 'r') as commons:
        for line in commons:
            guess = line.strip()
            if guess == actual_password:
                amtnotit += 1
                print(f"Got it from commons! Password is: {guess}")
                print(f"Took {amtnotit} tries!")
                sys.exit(0)

            # adds one to amtnotit counter
            amtnotit += 1

            if amtnotit % PROGRESS_INTERVAL == 0:
                print(f"Tried {amtnotit} guesses so far...")

# skips common pass check if commons.txt was not found
except FileNotFoundError:
    print("commons.txt not found, skipping common password check. maybe its in a different folder?")

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

# Loops through each possible length
for length in range(MIN_LENGTH, MAX_LENGTH + 1):
    for guess in product(chars, repeat=length):

        # Direct tuple comparison (no string creation here) (used to use string, nolonger does for speed)
        if guess == actual:
            amtnotit += 1
            print(f"Got it! Password is: {''.join(guess)}")
            print(f"Took {amtnotit} tries!")
            found = True
            break

        # adds one to amtnotit counter as done before
        amtnotit += 1

        if amtnotit % PROGRESS_INTERVAL == 0:
            print(f"Tried {amtnotit} guesses so far...")

    if found:
        break

if not found:
    print("\nPassword was not found in the brute-force search space.")
    print("Maybe it's too long, contains numbers, symbols, or uses unsupported characters.")

# Reminder:
# You can remove amtnotit and the progress check entirely for slightly better speed,
# but you won't see progress updates.
