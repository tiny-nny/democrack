# democrack!
ver 2.0

## Yes, this is the real repo. The repo was just moved from SchoolFlashCards5 to TheDemoProject.

# THIS IS ZACH'S PROJECT, NOT EK


# BIG OLD WARNING:
# THIS IS AN EDUCATION RESOURCE
# DO NOT USE IN REAL LIFE ON REAL PASSWORDS!
# I CANNOT STRESS THIS ENOUGH!
## This is, again, education proj. This is to teach people how crackers work and how to avoid having their passwords compromised.

### Only works with ascii letters (no symbols, no numbers, no punctuation. just letters)


democrack! is a democracker in pure python.

reminder:

as of update 1.2 ish, you only need one .py/.exe for it to function, but if you want to have a dictionary attack included, include the commons.txt in the same folder as the .py or .exe you are executing.

## Something to note

Once again, this is an educational resource, and do not use this on real accounts on real people.

Now that that's out of the way, democrack-withcomments.py and democrack-mildlyfaster.py are NOT needed, they are simply other versions (comments lets you get more of an idea of how it works, mildly faster removes the amtnotit variable and anything to do with it for a mild speed boost).


## Why?

Boredom and freedom can combine for the better or for the worse, and here? A little bit of a mix.

## Desktop version

This is the simplest thing i can POSSIBLY explain. It is a pyinstaller exe, so thanks to pyinstaller i could make a desktop version.

It is based of GUI, which is based off of the mildly-faster, which is based off democrack, so it somehow still all loops back to the original script.

And no, it ain't a virus. Your antivirus may say so though, considering it is a demo of a cracking tool (THAT IS A DEMO, EDUCATIONAL USES ONLY PEOPLE!). So if you get a warning from your antivirus or virustotal, run it in a virtual machine with wireshark open, believe me, it's fine.

## GUI 

<sub>(this was lowkey the hardest part)</sub>

I have no need to explain. It basically reroutes stuff from the terminal to the GUI before it even TRIES. Just does all the behind the scenes work normally and outputs in a cleaner fashion (for some people, i think the CLI version is better.)

GUI is based off of the mildly-faster version of democrack.

Just read below on how it works, and imagine a little traffic guy telling the code to go from the terminal to the GUI.

## How this silly democracker works

It begins with a selection area where you can choose the password type you want

1. Default to pass.txt password
2. User types in a password

This lets the user control the democracker much easier without having to directly edit the files that it kinda depends on.

Due to v1.2 changes, the pass.txt AND commons.txt are nolonger required, you need atleast one of the py files, because they are the democrackers (they are just different versions. Versions being:

1. Base democracker (democrack)

This is the normal version, outputs updates, democracks, the whole shabang.

2. Commented democracker (democrack-withcomments)

This version functions the same as the base democracker, but in the code it has a lot more comments so people can better understand how it works.

3. Mildly faster democracker (democrack-mildlyfaster)

This version removes the amtnotit var and everything about it, removing updates on guesses and guess amount at the end, but preserving the functionality of the program, to teach people how crackers work and how better passwords defend against such.


### How it actually works (option 1 selected)
Step 1.
The democracker (again, this is a demo) first asks for option selection, then if 1 is selected, it checks first if pass.txt exists, if not it cannot continue because it cannot default. Otherwise, it checks if commons.txt exists. If not, it skips to step 3. If it does, it goes to step 2.

Step 2.
The program then begins the common passwords check, or dictionary attack, which tries a bunch of easy passes. If it is not found there, it continues to step 3. If it is, it stops and prints fetched/guessed pass.

Step 3.
The program then begins brute forcing. This is pretty simple to understand and does not require a paragraph to explain.


### How it actually works (option 2 selected)
Step 1.
The democracker asks for input, but option 2 is selected. Then it asks for input on password. Once it gets that input, it goes to step 2.

Step 2.
The democracker then begins dictionary attack. It was explained earlier, do not need it here.

Step 3.
The democracker begins to brute force. This obviously, is the same as option 1 selection, but with the password you inputted.

### How it actually works (option 3 selected)
It generates a password, giving you the option between random garbled garbage, and readable and rememberable good passwords.

Not too much to go over here.



# CHANGE LOG

## v2.0 changes
Add little thing warning in some code that didnt have it thats like "Oh nozers! Couldnt find commons.txt/pass.txt, wrong folder maybe?"

Also added password generator, new thing that allows you to generate passwords to see what a good password *should* look like

## v1.3 changes
added warning, and desktop version (enough to warrant its own version in my opinion)

## v1.2 changes
Added ascii banner before anything else (displays "democrack!" in ascii art

Added selection between defaulting to pass.txt password and the user typing in a custom one (pass.txt no longer required!)

## v1.1 changes
Add faster file and update a few things (it was a while ago bro I forgot).


## Credits

Me on the code (This is my project, im Nny, but this IS a shared account)

BUT huge crerdits to Daniel Miessler 🛡️ for the passwords list 

His page is https://github.com/danielmiessler 

List was at https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10k-most-common.txt
