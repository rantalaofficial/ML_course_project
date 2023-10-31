import os
from os import listdir
from os.path import isfile, join, isdir
import random

import matplotlib.pyplot as plt

cleanedFolder = './cleanedDataset/'

# read all files inside cleanedDataset
files = [f for f in listdir(cleanedFolder) if isfile(join(cleanedFolder, f))]
print(files)

datasetLines = []

character_frequency_average = {}
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
    samples = list(filter(None, samples)) # remove empty strings

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

        
        # calculate relative frequency
        character_frequency = [round(f / len(sample) * 100) for f in character_frequency]
        datasetLines.append(label + ":" + ','.join(str(f) for f in character_frequency))

        # calculate average for each language
        if label not in character_frequency_average:
            character_frequency_average[label] = [0] * 1000
        character_frequency_average[label] = [character_frequency_average[label][i] + (character_frequency[i] / len(samples)) for i in range(len(character_frequency))]

    print('Finished extracting features from ' + str(len(samples)) + ' code samples to ' + file)

# mix datasetLines randomly
random.shuffle(datasetLines)

f = open('./languageFeatures.txt', 'w')
f.write('\n'.join(str(line) for line in datasetLines))
f.close()

for language in character_frequency_average:
    plt.plot(character_map, character_frequency_average[language][:len(character_map)], label=language)

plt.xlabel('Character')
plt.ylabel('Relative Frequency (%)')
plt.legend()
plt.show()