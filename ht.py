import os
import re
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

def tSpace(color=colors.blue): # function for printing bar across screen, optionally color argument
    print(color, end="")
    termSize = os.get_terminal_size(0)
    print("-"*termSize.columns)
    print(colors.normal, end="")

def tHeader(string, bColor=colors.blue, tColor=colors.purple):
    termSize = os.get_terminal_size(0)
    strLen = len(string)
    padding = int((termSize.columns - strLen) / 2)
    print(bColor, end="")
    print("-"*padding, end="")
    print(tColor + string, end="")
    print(bColor, end="")
    print("-"*padding + colors.normal)

def tBox(string, bColor=colors.blue, tColor=colors.purple):
    termSize = os.get_terminal_size(0)
    if "\n" not in string: # Normal Method
        strLen = len(string)
        if strLen <= (termSize.columns -2): # if the string is smaller than the width of the terminal
            print(bColor + "+" + "-"*strLen + "+") # Print the top of the box
            print(bColor + "|" + tColor + string + bColor + "|")
            print(bColor + "+" + "-"*strLen + "+" + colors.normal) # Print the bottom of the box
        else: # if the string is larger than the width of the terminal
            tSpace(bColor)
            print(tColor + string)
            tSpace(bColor)
    else: # If it contains multiple lines
        strippedString = string
        string = string.split('\n') # Split the string based on newline characters
        # Strip 7-bit C1 ANSI sequences, taken from https://stackoverflow.com/a/14693789
        ansi_escape = re.compile(r'''
\x1B  # ESC
(?:   # 7-bit C1 Fe (except CSI)
[@-Z\\-_]
|     # or [ for CSI, followed by a control sequence
    \[
    [0-?]*  # Parameter bytes
    [ -/]*  # Intermediate bytes
    [@-~]   # Final byte
)
''', re.VERBOSE)
        strippedString = ansi_escape.sub('', strippedString)
        strippedString = strippedString.split('\n')
        strLen = len(max(strippedString, key=len)) # find the length of the greatest string
        print(bColor + "+" + "-"*strLen + "+") # Print the top of the box
        for i in string:
            if len(i) != strLen:
                i = i + " "*(strLen - len(i))
            print(bColor + "|" + tColor + i + bColor + "|")
        print(bColor + "+" + "-"*strLen + "+" + colors.normal) # Print the bottom of the box
