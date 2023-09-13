import os
from os import listdir
from os.path import isfile, join, isdir

languagesFolder = './languagesDataset/'

STARTING_MARKER = '<textarea autocomplete="off" id="textareaCode" wrap="logical" spellcheck="false">'
ENDING_MARKER = '</textarea>'

# get all folders inside the languages folder
languages = [f for f in listdir(languagesFolder) if isdir(join(languagesFolder, f))]

print(languages)

# get all files inside each language folder
for language in languages:
    files = [f for f in listdir(languagesFolder + language) if isfile(join(languagesFolder + language, f))]

    language_code_examples = ""

    # if filename begins with try, open it
    for file in files:
        if file.startswith('try') or file.startswith('phptry'): # phptry is for php files

            # open file
            try:
                f = open(languagesFolder + language + '/' + file, 'r')
                contents = f.read()
                f.close()
            except:
                print('Error reading file: ' + file)
                continue
            
            contents = contents[contents.find(STARTING_MARKER)+len(STARTING_MARKER):]
            contents = contents[:contents.find(ENDING_MARKER)]
            
            # check if contents has a div tag, meaning the parsing has failed
            if contents.find('<div') != -1:
                print('Error parsing file: ' + file)
                continue
            
            language_code_examples += contents + "\nEND_OF_CODE\n"

    # save to file
    f = open('./cleanedDataset/' + language + '.txt', 'w')
    f.write(language_code_examples)
    f.close()
