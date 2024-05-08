import json
import os.path

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

cards = []
flashNum = 0
AiThreshold = 2.5 # default val, cfgFile overides it
isAiCompImported = False
usingAi = False
jsonFile = "sets/set.json"
cfgFile = "cfg.json"
def yn(q):
    i = input(q + "\n(Y/N): ")
    i = i.lower()
    if i == "y":
        global result
        result = True
    elif i == "n":
        result = False
    else:
        print(colors.warn + "Please enter: Y,N,y,n" + colors.normal)
        prgExit()
    return result

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
def termSpace(): # function for printing 2 newlines
    print(colors.blue, end="")
    termSize = os.get_terminal_size(0)
    for i in range(termSize.columns):
        print("-", end="")
    print(colors.normal, end="")

def saveJson():
    #jsonObj = json.dumps(cards[0].term, indent=4)
    jsonObj = json.dumps(cards, indent=4)
    with open(jsonFile, "w") as outFile:
        outFile.write(jsonObj)
def readJson():
    with open(jsonFile, "r") as inFile:
        jsonStr = inFile.read()
        jCards = json.loads(jsonStr)
    global cards
    cards = jCards
    #print(jCards)

def readCfg(): # read config file
    global cfg, AiThreshold, autoloadSets
    with open(cfgFile, "r") as inFile:
        global cfg
        cfgStr = inFile.read()
        cfg = json.loads(cfgStr)
    print("---Config File---")
    print(cfg)
    AiThreshold = cfg['AiThreshold']
    autoloadSets = cfg['autoloadSets']

def saveCfg():
    cfgObj = json.dumps(cfg, indent=4)
    with open(cfgFile, "w") as outFile:
        outFile.write(cfgObj)
    readCfg() # update values

def createCfg(): # creates config file, OVERWRITES CONFIG FILE
    global cfg, isAiCompImported
    usingAi = yn("Do you want to use AI to compare term/definition?")
    if usingAi == True:
        import aicomp
        isAiCompImported = True
    cfg = {'UsesAI': usingAi, 'autoloadSets': True, 'AiThreshold': AiThreshold}
    saveCfg()

def cfgMenu():
    global cfg
    print("Welcome to Config Menu\nCurrent Config:")
    termSpace()
    print(cfg)
    termSpace()
    i = input("What would you like to change?\n: ")
    print(i, "=", cfg[i])
    print("Type:", type(i))
    v = input("What would you like the value to be?\n: ")
    if type(cfg[i]) == int:
        v = int() # make input an int
    elif type(cfg[i]) == bool:
        if v == "True":
            v = True
        elif v == "False":
            v = False
        else:
            print(colors.warn + "Please enter either " + colors.normal + colors.blue + "True" + colors.normal + "/" + colors.red + "False" + colors.normal)
    cfg[i] = v
    saveCfg()
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
            if compare(defin, answer) == True:
                print("Correct!")
            print("[AI] Incorrect")
def prgExit():
    saveCfg()
    print(colors.normal , end="")
    exit()
def help():
    print("""
V => View Flashcard
T => Test Flashcard
Y => Test with Ai 
M => Make Flashcard
A => List all Flashcards
S => Save Flashcard
R => Read Flashcard""")
print("Welcome to Flashcard Maker")
if os.path.exists(cfgFile):
    readCfg()
else: 
    createCfg()
if cfg['UsesAI'] == True:
    import aicomp
if cfg['autoloadSets'] == True:
    readJson()
else:
    print("Could not find Config File, creating one")
    createCfg()
help()
while True:
    if flashNum == 0:
        print("Press M to Make Flashcards")
    else:
        #print("Enter V to View Flashcards, Enter T to Test Flashcards, Enter Y to Test with AI, or M to make more")
        help()
    i = (input(": ")).lower()
    if i == "m":
        makeFlash()
    elif i == "v":
        cardNum = input("What Card?: ")
        if cardNum == "":
            prgExit()
        cardNum = int(cardNum) - 1
        printFlash(cardNum)
    elif i == "t":
        cardNum = input("What Card? There are " + str(len(cards)) + " Card(s): ")
        if cardNum == "":
            prgExit()
        cardNum = int(cardNum) - 1
        quizFlash(cardNum)
    elif i == "y":
        usingAi = True
        cardNum = input("What Card? There are " + str(len(cards)) + " Card(s): ")
        if cardNum == "":
            prgExit()
        cardNum = int(cardNum) - 1
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
    elif i == "c":
        cfgMenu()
    else:
        print(colors.warn + "Invalid Option" + colors.normal)
