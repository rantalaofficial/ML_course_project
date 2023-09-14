import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import matplotlib.pyplot as plt

# read all lines of languageFeatures.txt
f = open('./languageFeatures.txt', 'r')
contents = f.read()
f.close()

lines = contents.split('\n')

y = []
X = []

for line in lines:
    if line == '':
        continue
    split = line.split(':')
    y.append(split[0])
    X.append(split[1].split(','))

# convert y to numbers
languages = list(set(y))
for i in range(len(y)):
    y[i] = languages.index(y[i])

# convert to numpy array
X = np.array(X, dtype=np.float32)
y = np.array(y)

# split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)

rfModel = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=0, verbose=1, criterion='gini')
rfModel.fit(X_train, y_train)

SVCModel = SVC(kernel='linear', C=1.0, random_state=0, verbose=1)
SVCModel.fit(X_train, y_train)

def calculateAccuracy(predictions, y_test):
    correct = 0
    for i in range(len(predictions)):
        if round(predictions[i]) == y_test[i]:
            correct += 1

    # calculate accuracies for each language
    language_correct = [0] * len(languages)
    language_total = [0] * len(languages)

    for i in range(len(predictions)):
        language_total[y_test[i]] += 1
        if round(predictions[i]) == y_test[i]:
            language_correct[y_test[i]] += 1

    return [round(language_correct[i]/language_total[i]*1000) / 10 for i in range(len(languages))]

rfAccuracy = calculateAccuracy(rfModel.predict(X_test), y_test)
SVCModelAccuracy = calculateAccuracy(SVCModel.predict(X_test), y_test)

fig, ax = plt.subplots()
index = np.arange(len(languages))
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, rfAccuracy, bar_width, alpha=opacity, color='b')
rects2 = plt.bar(index + bar_width, SVCModelAccuracy, bar_width, alpha=opacity, color='g')

plt.xlabel('Language')
plt.ylabel('Accuracy')
plt.title('Accuracy by language and model. Blue = Random Forest, Green = SVC')
plt.xticks(index + bar_width, languages)

for i in range(len(languages)):
    plt.text(i-0.05, rfAccuracy[i] + 1, str(rfAccuracy[i]) + '%', ha='center', va='bottom')
    plt.text(i + bar_width+0.05, SVCModelAccuracy[i] + 1, str(SVCModelAccuracy[i]) + '%', ha='center', va='bottom')

fig = plt.gcf()
fig.set_size_inches(12, 5)
plt.show()


