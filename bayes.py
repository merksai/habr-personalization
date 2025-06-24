from collections import Counter, defaultdict
from math import log


class NaiveBayesClassifier:

    def __init__(self, alpha=0.01):
        self.alpha = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.classes_ = set(y)

        self.p_classes = {}
        cnt = Counter(y)
        for class_ in self.classes_:
            self.p_classes[class_] = cnt[class_] / len(y)

        words = defaultdict(int)
        self.table = {class_: defaultdict(int) for class_ in self.classes_}

        for x, label in zip(X, y):
            for word in x.split():
                self.table[label][word] += 1
                words[word] += 1

        self.d = len(words)

        self.n_c = {class_: sum(self.table[class_].values()) for class_ in self.classes_}

        self.table = {
            class_: {
                word: (count + self.alpha) / (self.n_c[class_] + self.alpha * self.d)
                for word, count in self.table[class_].items()
            }
            for class_ in self.classes_
        }

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        pred = []
        for x in X:
            p = {class_: log(self.p_classes[class_]) for class_ in self.classes_}

            for word in x.split():
                for class_ in self.classes_:
                    word_prob = self.table[class_].get(word, self.alpha / (
                                self.n_c[class_] + self.alpha * self.d))
                    p[class_] += log(word_prob)

            pred.append(max(p, key=p.get))

        return pred

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        pred = self.predict(X_test)
        true = sum(pred_i == true_i for pred_i, true_i in zip(pred, y_test))
        accuracy = true / len(y_test)
        return round(accuracy, 12)