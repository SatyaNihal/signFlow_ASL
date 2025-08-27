import pickle
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

dataDict = pickle.load(open('./data.pickle', 'rb'))

# converting the data to numpy array
data = np.asarray(dataDict['data'])
labels = np.asarray(dataDict['labels'])

x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

model = ExtraTreesClassifier(n_estimators=300) #use 300 random trees

model.fit(x_train, y_train)  # training the classifier

y_predict = model.predict(x_test)  # making the prediction

score = accuracy_score(y_predict, y_test)

print('{}% of the samples were classified correctly:'.format(score * 100))

# saving the model
f = open('model.p', 'wb')
pickle.dump({'model': model}, f)
f.close()
