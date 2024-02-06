import json

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

#class flashcard:
#    def __init__(self, term, defin):
#        self.term = term
#        self.defin = defin
#    def __call__(self, term, defin):
#        self.term = term
#        self.defin = defin
cards = []
flashNum = 0
AiThreshold = 2.5
isAiCompImported = False
usingAi = False
jsonFile = "set.json"
def makeFlash():
    global flashNum
    term = input("Term: ")
    defin = input("Definition: ")
    card = dict(term = term, defin = defin)
    cards.append(card)
    #cards.append(flashcard(term, defin))
    flashNum += 1

def printFlash(cardNum):
    #print("Term:", cards[cardNum].term)
    #print("Defin:", cards[cardNum].defin)
    print("Term: " + cards[cardNum].get("term"))
    print("Definition: " + cards[cardNum].get("defin"))

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
        print(card)
def saveJson():
    #jsonObj = json.dumps(cards[0].term, indent=4)
    jsonObj = json.dumps(cards, indent=4)
    with open(jsonFile, "w") as outfile:
        outfile.write(jsonObj)
def readJson():
    with open(jsonFile, "r") as infile:
        jsonStr = infile.read()
        jCards = json.loads(jsonStr)
    global cards
    cards = jCards
    print(jCards)
def quizFlash(cardNum):
    cardNum = int(cardNum)
    #card = cards[cardNum]
    term = cards[cardNum].get("term")
    defin = cards[cardNum].get("defin")
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
        result = aicomp.AiCompare(defin, answer)
        print(f"[AI]: {result}")
        if result >= AiThreshold: # type: ignore
            print("[AI] Correct!")
        else:
            print("[AI] Incorrect")
def prgExit():
    print(colors.normal , end="")
    exit()
def help():
    print("""
V => View Flashcard
T => Test Flashcard
Y => Test with Ai 
M => Make Flashcard
S => Save Flashcard
R => Read Flashcard""")
while True:
    print("Welcome to Flashcard Maker")
    if isAiCompImported == False:
        i = input("AI is not imported, do you want to import it? (Y/N): ")
        i = i.strip().lower()
        if i == "y":
            print("Importing AI (this might take a second)")
            import aicomp
            isAiCompImported = True
        else:
            print("AI Functions will not be accessible")
    if flashNum == 0:
        print("Press M to Make Flashcards")
    else:
        #print("Enter V to View Flashcards, Enter T to Test Flashcards, Enter Y to Test with AI, or M to make more")
        help()
    i = (input(": ")).lower()
    if i == "m":
        makeFlash()
    elif i == "v":
        cardNum = int(input("What Card?: "))
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
    elif i == "s":
        print(f"Saving JSON to {jsonFile}")
        saveJson()
    elif i == "r":
        print(f"Reading from {jsonFile}")
        readJson()
    else:
        print(colors.warn + "Invalid Option" + colors.normal)
