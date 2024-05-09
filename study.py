import json
import os.path
import ht
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
cursor = colors.purple + ": " + colors.normal
sep = " | "
isAiCompImported = False
usingAi = False
jsonFile = "sets/set.json"
cfgFile = "cfg.json"
def yn(q):
    i = input(q + "\n(Y/N)" + cursor)
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
    term = input("Term" + cursor)
    defin = input("Definition" + cursor)
    card = dict(term = term, defin = defin, correct = 0, incorrect = 0)
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
        cardStr = f"Term: {card['term']}" + sep
        cardStr += f"Defin: {card['defin']}" + "\n"
        cardStr += f"Correct: {card['correct']}" + sep
        cardStr += f"Incorrect: {card['incorrect']}"
        ht.tBox(cardStr, colors.cyan, colors.yellow)

def saveJson():
    #jsonObj = json.dumps(cards[0].term, indent=4)
    jsonObj = json.dumps(cards, indent=4)
    with open(jsonFile, "w") as outFile:
        outFile.write(jsonObj)
def readJson():
    if os.path.exists(jsonFile):
        with open(jsonFile, "r") as inFile:
            jsonStr = inFile.read()
            jCards = json.loads(jsonStr)
        global cards
        cards = jCards
        #print(jCards)
    else:
        ht.tBox(f"No JSON file Found! at {jsonFile}", colors.yellow, colors.red)

def readCfg(): # read config file
    global cfg, AiThreshold, autoloadSets, usingAi
    with open(cfgFile, "r") as inFile:
        global cfg
        cfgStr = inFile.read()
        cfg = json.loads(cfgStr)
    #ht.tHeader("Config File")
    #print(colors.cyan, end="")
    #print(cfg)
    #ht.tSpace()
    AiThreshold = float(cfg['AiThreshold'])
    autoloadSets = cfg['autoloadSets']
    usingAi = cfg['usesAi']

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
    cfg = {'usesAi': usingAi, 'autoloadSets': True, 'AiThreshold': AiThreshold, 'help': True}
    saveCfg()

def cfgMenu():
    global cfg
    ht.tHeader("Welcome to Config Menu")
    print("Current Config:" + colors.purple)
    print(cfg)
    ht.tSpace()
    i = input(colors.blue + "What would you like to change?" + colors.normal + "\n" + cursor)
    if i == "":
        return None
    print(i, "=", cfg[i])
    v = input("What would you like the value to be? " + colors.warn + "Case Sensitive!" + colors.normal + "\n" + cursor)
    cfg[i] = v
    saveCfg()

def quizFlash(cardNum):
    global correct, incorrect

    cardNum = int(cardNum)
    #card = cards[cardNum]
    term = cards[cardNum].get("term")
    defin = cards[cardNum].get("defin")
    correct = cards[cardNum].get("correct")
    incorrect = cards[cardNum].get("incorrect")
    ht.tBox(term)
    answer = input(cursor)
    if usingAi == False:
        if compare(defin, answer) == True:
            print("Correct!")
            cards[cardNum]["correct"] = correct + 1
        else:
           print("Incorrect!")
           cards[cardNum]["incorrect"] = incorrect + 1
    else:
        global isAiCompImported
        result = aicomp.AiCompare(defin, answer)
        print(f"[AI]: {result}")
        if result >= AiThreshold: # type: ignore
            print("[AI] Correct!")
            cards[cardNum]["correct"] = correct + 1
        else:
            if compare(defin, answer) == True:
                print("Correct!")
                cards[cardNum]["correct"] = correct + 1
            print("[AI] Incorrect!")
            cards[cardNum]["incorrect"] = incorrect + 1

def prgExit():
    saveCfg()
    print(colors.normal , end="")
    exit()

def help():
    help = ""
    if flashNum > 0:
        help = colors.blue + "V => View Flashcard \nA => List all Cards\n" + colors.green + "T => Test Flashcard \n"
        if usingAi:
            help += colors.purple + "T => Test with AI   \n"
    help += colors.yellow + "S => Save Flashcards\n"
    help += "R => Read Flashcards\n"
    help += colors.purple + "M => Make Flashcard " + colors.normal
    ht.tBox(help)

ht.tHeader("Welcome to Flashcard Maker!", colors.green, colors.blue)

if os.path.exists(cfgFile):
    readCfg()
else: 
    createCfg()
if cfg['usesAi'] == True:
    import aicomp
if cfg['autoloadSets'] == True and os.path.exists(jsonFile):
    readJson()
flashNum = len(cards)
while True:
    #print("Enter V to View Flashcards, Enter T to Test Flashcards, Enter Y to Test with AI, or M to make more")
    if cfg['help']:
        help()
    i = (input(cursor)).lower()
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
