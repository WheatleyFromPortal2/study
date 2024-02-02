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
    #flashcard = flashcard(term, defin)
    cards.append(flashcard(term, defin))
    flashNum += 1

def printFlash(cardNum):
    card = cards[cardNum]
    term = card.term
    defin = card.defin
    #print("Term:", term)
    #print("Definition", defin)
    print("Term:", cards[cardNum].term)
    print("Defin:", cards[cardNum].defin)

def compare(answer, inputed):
    #modify inputed
    inputed = inputed.strip()
    inputed = inputed.lower()
    inputed = inputed.replace(".", " ")
    inputed = inputed.replace(",", " ")
    inputed = inputed.replace("-", " ")
    inputed = inputed.replace("/", " ")
    #modify answer
    answer = answer.strip()
    answer = answer.lower()
    answer = answer.replace(".", " ")
    answer = answer.replace(",", " ")
    answer = answer.replace("-", " ")
    answer = answer.replace("/", " ")
    #compare both
    if answer == inputed:
        return True
    else:
        return False
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
    if compare(defin, answer) == True:
        print("Correct!")
    else:
        print("Incorrect")
def prgExit():
    print(colors.normal , end="")
    exit()
while True:
    print("Welcome to Flashcard Maker")
    if flashNum == 0:
        print("Press M to Make Flashcards")
    else:
        print("Enter V to View Flashcards, Enter T to Test Flashcards, or M to make more")
    i = (input(": ")).lower()
    if i == "m":
        makeFlash()
    elif i == "v":
        cardNum = int(input("What Card? "))
        if cardNum == "":
            prgExit()
        printFlash(cardNum)
    elif i == "t":
        cardNum = int(input("What Card? There are " + str(flashNum) + " Card(s): "))
        if cardNum == "":
            prgExit()
        quizFlash(cardNum)
    elif i == "":
        prgExit()
    elif i == "a":
        printAllCards()
    else:
        print(colors.warn + "Invalid Option" + colors.normal)
