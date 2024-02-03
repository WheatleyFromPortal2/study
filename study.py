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
AiThreshold = 2.5
isAiCompImported = False
usingAi = False
def makeFlash():
    global flashNum
    term = input("Term: ")
    defin = input("Definition: ")
    #flashcard = flashcard(term, defin)
    cards.append(flashcard(term, defin))
    flashNum += 1

def printFlash(cardNum):
    print("Term:", cards[cardNum].term)
    print("Defin:", cards[cardNum].defin)

def compare(answer, inputed):
    #modify inputed
    inputed = inputed.strip()
    inputed = " " + inputed + " "
    inputed = inputed.lower()
    inputed = inputed.replace(".", " ")
    inputed = inputed.replace(",", " ")
    inputed = inputed.replace("-", " ")
    inputed = inputed.replace("/", " ")
    inputed = inputed.replace(" and ", " ")
    inputed = inputed.replace(" an ", " ")
    inputed = inputed.replace(" a ", " ")
    inputed = inputed.replace(" some ", " ")
    inputed = inputed.strip()
    #modify answer
    answer = answer.strip()
    answer = " " + answer + " "
    answer = answer.lower()
    answer = answer.replace(".", " ")
    answer = answer.replace(",", " ")
    answer = answer.replace("-", " ")
    answer = answer.replace("/", " ")
    answer = answer.replace(" and ", " ")
    answer = answer.replace(" an ", " ")
    answer = answer.replace(" a ", " ")
    answer = answer.replace(" some ", " ")
    answer = answer.strip()
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
    if usingAi == False:
        if compare(defin, answer) == True:
            print("Correct!")
        else:
           print("Incorrect")
    else:
        global isAiCompImported
        #if isAiCompImported == False:
        #    import aicomp
        #    isAiCompImported = True      
        if aicomp.AiCompare(defin, answer) >= AiThreshold: # type: ignore
            print("[AI] Correct!")
        else:
            print("[AI] Incorrect")
def prgExit():
    print(colors.normal , end="")
    exit()
while True:
    print("Welcome to Flashcard Maker")
    if isAiCompImported == False:
        i = input("Ai is not imported, do you want to import it? (Y/N)")
        i = i.strip().lower()
        if i == "y":
            print("Importing AI (this might take a second)")
            import aicomp
            isAiCompImported = True
        else:
            print("Ai Functions will not be accessible")
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
    elif i == "y":
        usingAi = True
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
