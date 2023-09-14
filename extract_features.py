import os
from os import listdir
from os.path import isfile, join, isdir
import random

cleanedFolder = './cleanedDataset/'

# read all files inside cleanedDataset
files = [f for f in listdir(cleanedFolder) if isfile(join(cleanedFolder, f))]
print(files)

datasetLines = []

# read each file
for file in files:
    try:
        f = open(cleanedFolder + file, 'r')
        contents = f.read()
        f.close()
    except:
        print('Error reading file: ' + file)
        continue
    
    # remove new lines and spaces
    contents = contents.replace('\n', '').replace(' ', '')

    samples = contents.split('END_OF_CODE')

    # remove empty strings
    samples = list(filter(None, samples))    

    character_map = []
    character_frequency = []

    label = file.split('.')[0]

    # count character frequency
    for sample in samples:

        character_frequency = [0] * 1000

        for character in sample:
            if character not in character_map:
                character_map.append(character)
                character_frequency[len(character_map)-1] += 1
            else:
                character_frequency[character_map.index(character)] += 1

        total_characters = len(sample)
        # relative frequency is in percentages
        character_frequency = ','.join(str(round(f / total_characters * 100)) for f in character_frequency)

        datasetLines.append(label + ":" + character_frequency)

    print('Finished extracting features from ' + str(len(samples)) + ' code samples to ' + file)

# mix datasetLines randomly
random.shuffle(datasetLines)

f = open('./languageFeatures.txt', 'w')
f.write('\n'.join(str(line) for line in datasetLines))
f.close()