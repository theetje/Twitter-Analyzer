""" Return een array met daarin de woorden voor analyse. """
def getWordsFromLexicons(input_file):
    f = open(input_file)
    temp_array = []

    for lines in f:
        if ';' not in lines: # haal de comments weg
            temp_array.append(lines.rstrip())

    return temp_array

def tweetConstraint(tweet, language, key_word):
    if 'lang' in tweet: # Kijk of in de tweet de taal word aangegeven
        if tweet['lang'] == language: # Kijk of de taal in de tweet engels is
            # Je kan hier kijken of je controleerd of er een geldige taal word opgegeven.
            if key_word in tweet['text'].lower():
                return tweet
