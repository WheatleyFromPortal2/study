class colors:
    red = '\033[91m'
    green = '\033[92m'
    blue = '\033[94m'
    purple = '\033[95m'
    cyan = '\033[96m'
    yellow = '\033[93m'
    normal = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'
    warn = '\033[91m\033[1m\033[4m'

class flashcard:
    def __init__(self, term, defin):
        self.term = term
        self.defin = defin
    def __call__(self, term, defin):
        self.term = term
        self.defin = defin
cards = []
flashNum = 0

def makeFlash():
    global flashNum
    global flashcard
    term = input("Term: ")
    defin = input("Definition: ")
    flashcard = flashcard(term, defin)
    cards.append(flashcard)
    flashNum += 1

def printFlash(cardNum):
    card = cards[cardNum]
    term = card.term
    defin = card.defin
    print("Term:", term)
    print("Definition", defin)


def printAllCards():
    for card in cards:
        print("Index", cards.index(card))
        print("Term:", card.term)
        print("Definition:", card.defin)

def quizFlash(cardNum):
    cardNum = int(cardNum)
    card = cards[cardNum]
    term = card.term
    defin = card.defin
    answer = input(term + ": ")
    if answer == defin:
        print("Correct!")
    else:
        print("Incorrect")
def prgExit():
    exit()
while True:
    print("Welcome to Flashcard Maker")
    if flashNum == 0:
        print("Press M to Make Flashcards")
    else:
        print("Enter V to View Flashcards, Enter T to Test Flashcards")
    i = (input(": ")).lower()
    if i == "m":
        makeFlash()
    elif i == "v":
        cardNum = input("What Card? ")
        printFlash(0)
    elif i == "t":
        cardNum = int(input("What Card? There are " + str(flashNum) + " Card(s)"))
        quizFlash(cardNum)
    elif i == "":
        prgExit()
    elif i == "a":
        printAllCards()
    else:
        print(colors.warn + "Invalid Option" + colors.normal)
