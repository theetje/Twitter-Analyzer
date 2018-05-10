import requests

""" Return een array met daarin de woorden voor analyse """
def getWordsFromLexicons(input_file):
    f = open(input_file)
    temp_array = []

    for lines in f:
        if ';' not in lines: # haal de comments weg
            temp_array.append(lines.rstrip())

    return temp_array
