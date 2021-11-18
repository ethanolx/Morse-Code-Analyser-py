# Name:     Ethan Tan
# Admin:    P2012085
# Class:    DAAA/2B/03

## ENTRY POINT TO MAIN PROGRAM ##

# run "python ." or "python __main__.py" from this directory

# Import the main object
from tools.morse_code_analyser import Morse_Code_Analyser
from tools.data_structures.stack import Stack
from tools.sorting.quicksort import quicksort

# Declare a custom configuration dictionary
CONFIG = {
    "author": {
        "name": "Ethan Tan",
        "admin": "2012085",
        "class": "DAAA/2B/03",
        "module": "ST1507 DSAA",
    },
    "min_significant_frequency": 2
}

# Instantiate the analyser object and run it
morse_code_analyser = Morse_Code_Analyser(config=CONFIG)
morse_code_analyser.run()
