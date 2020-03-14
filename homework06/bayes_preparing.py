import codecs
import string

def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


def data_preparing():
    file = codecs.open("data\\SMSSpamCollection", "r", "utf-8")
    data = file.read()
    file.close()

    data = data.split("\r\n")

    new_data = []
    for el in data:
        new_data.append(el.split("\t"))

    del new_data[-1]

    X, y = [], []
    for target, msg in new_data:
        X.append(msg)
        y.append(target)

    X = [clean(x).lower() for x in X]

    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]
    
    return X_train, y_train, X_test, y_test


def data_preparing_test():

    train = [
        ('I love this sandwich.', 'pos'),
        ('This is an amazing place!', 'pos'),
        ('I feel very good about these beers.', 'pos'),
        ('This is my best work.', 'pos'),
        ("What an awesome view", 'pos'),
        ('I do not like this restaurant', 'neg'),
        ('I am tired of this stuff.', 'neg'),
        ("I can't deal with this", 'neg'),
        ('He is my sworn enemy!', 'neg'),
        ('My boss is horrible.', 'neg')
    ]
    test = [
        ('The beer was good.', 'pos'),
        ('I do not enjoy my job', 'neg'),
        ("I ain't feeling dandy today.", 'neg'),
        ("I feel amazing!", 'pos'),
        ('Gary is a friend of mine.', 'pos'),
        ("I can't believe I'm doing this.", 'neg')
    ]

    X_train, y_train, X_test, y_test = [], [], [], []

    for msg, target in train:
        X_train.append(msg)
        y_train.append(target)

    for msg, target in test:
        X_test.append(msg)
        y_test.append(target)

    X_train = [clean(x).lower() for x in X_train]
    X_test = [clean(x).lower() for x in X_test]

    return X_train, y_train, X_test, y_test
