# Name:     Ethan Tan
# Admin:    P2012085
# Class:    DAAA/2B/03

## MAIN PROGRAM ##

from tools.morse_code_analyser import Morse_Code_Analyser

CONFIG = {
    "author": {
        "name": "Ethan Tan",
        "admin": "2012085",
        "class": "DAAA/2B/03",
        "module": "ST1507 DSAA",
    }
}

morse_code_analyser = Morse_Code_Analyser(config=CONFIG)
morse_code_analyser.run()
