import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split

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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8)

# train
clf = linear_model.LinearRegression()
clf.fit(X_train, y_train)

# test
predictions = clf.predict(X_test)

# print results
print('Predictions: ')
print(predictions)
print('Actual: ')
print(y_test)

# calculate accuracy
correct = 0
for i in range(len(predictions)):
    if round(predictions[i]) == y_test[i]:
        correct += 1

print('Accuracy: ' + str(correct/len(predictions)*100) + '%')

# calculate accuracies for each language
language_correct = [0] * len(languages)
language_total = [0] * len(languages)

for i in range(len(predictions)):
    language_total[y_test[i]] += 1
    if round(predictions[i]) == y_test[i]:
        language_correct[y_test[i]] += 1

for i in range(len(languages)):
    print(languages[i] + ': ' + str(language_correct[i]/language_total[i]*100) + '%')
    