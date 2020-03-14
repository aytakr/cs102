from bayes_preparing import data_preparing
from bayes_preparing import data_preparing_test

from db import News, session

from numpy import log as ln

class NaiveBayesClassifier:

    def __init__(self, alpha):
        self.alpha = alpha
        self.data = []
        self.data_count = []
        self.data_count_pos = []
        self.data_count_neg = []
        self.data_count_mb = []
        self.P_pos, self.P_neg = 0, 0
        self.P_mb = 0
        self.label = ['good', 'maybe', 'never']

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """

        for msg in X:
            for word in msg.split():
                if word not in self.data:
                    self.data.append(word)
                    self.data_count.append(1)
                    self.data_count_pos.append(0)
                    self.data_count_neg.append(0)
                    self.data_count_mb.append(0)

                else:
                    self.data_count[self.data.index(word)] += 1

                if y[X.index(msg)] == 'good':
                    self.data_count_pos[self.data.index(word)] += 1
                elif y[X.index(msg)] == 'maybe':
                    self.data_count_mb[self.data.index(word)] += 1
                else:
                    self.data_count_neg[self.data.index(word)] += 1

            if y[X.index(msg)] == 'good':
                self.P_pos += 1
            elif y[X.index(msg)] == 'maybe':
                self.P_mb += 1
            else:
                self.P_neg += 1

        self.P_pos = self.P_pos/len(X)
        self.P_neg = self.P_neg/len(X)
        self.P_mb = self.P_mb/len(X)

        self.P_w_pos = [0 for i in range(len(self.data))]
        self.P_w_neg = [0 for i in range(len(self.data))]
        self.P_w_mb = [0 for i in range(len(self.data))]

        for i in range(len(self.data)):
            self.P_w_pos[i] = (self.data_count_pos[i] + self.alpha)/(sum(self.data_count_pos) + self.alpha * len(self.data_count))
            self.P_w_neg[i] = (self.data_count_neg[i] + self.alpha)/(sum(self.data_count_neg) + self.alpha * len(self.data_count))
            self.P_w_mb[i] = (self.data_count_mb[i] + self.alpha)/(sum(self.data_count_mb) + self.alpha * len(self.data_count))

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        self.y_predict = [0 for i in range(len(X))]
        for msg in X:
            ln_P_pos = ln(self.P_pos)
            ln_P_neg = ln(self.P_neg)
            ln_P_mb = ln(self.P_mb)

            for word in msg.split():
                if word in self.data:
                    ln_P_pos += ln(self.P_w_pos[self.data.index(word)])
                    ln_P_neg += ln(self.P_w_neg[self.data.index(word)])
                    ln_P_mb += ln(self.P_w_mb[self.data.index(word)])

            if ln_P_pos >= ln_P_neg and ln_P_pos >= ln_P_mb:
                y_predict = 'good'
            elif ln_P_neg >= ln_P_pos and ln_P_neg >= ln_P_mb:
                y_predict = 'never'
            else:
                y_predict = 'maybe'

            self.y_predict[X.index(msg)] = y_predict

        return self.y_predict

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        scores = 0
        for i in range(len(y_test)):
            if self.y_predict[i] == y_test[i]:
                scores +=1

        return scores/len(y_test)

model = NaiveBayesClassifier(1)
#X_train, y_train, X_test, y_test = data_preparing()
s.
X_train, y_train, X_test, y_test =
model.fit(X_train, y_train)
model.predict(X_test)
