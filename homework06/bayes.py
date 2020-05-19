import math


class NaiveBayesClassifier:
    aprior_massive = []
    words = []
    s  = []
    priznak_index = {}
    index_priznak = {}
    def __init__(self, alpha=1):
        pass

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        words = []
        priznak_index = {}
        priznak_count = []
        s = set(y)
        self.s = s
        prisnak = [0 for i in range(len(s))]
        priznak_count = [0 for i in range(len(s))]
        self.aprior_massive = [0 for i in range(len(s))]
        for num,i in enumerate(s):
            priznak_index[i] = num
            self.index_priznak[num] = i
        self.priznak_index = priznak_index
        for nunnun in y:
            ind = priznak_index[nunnun]
            priznak_count[ind]+=1
        for u, i in enumerate(priznak_count):
            h = math.log10(i/(len(y)))
            self.aprior_massive[u]+=h
        for num, a in enumerate(X):
            slova_razdel = a.split()
            for h in slova_razdel:
                flag = True
                for num_1, word in enumerate(words):
                    if h == word[0]:
                        label = y[num]
                        label_ind = list(s).index(label)
                        words[num_1][label_ind + 1] += 1
                        flag = False
                        break
                if flag:
                    words.append([h] + [0 for _ in range(len(s))])
                    label = y[num]
                    label_ind = list(s).index(label)
                    words[len(words) - 1][label_ind + 1] += 1
        for num_3 in words:
            for chislo, stroka in enumerate(num_3[1:]):
                prisnak[chislo] += stroka
        for num_2, b in enumerate(words):
            p_massive = []
            for num_4,data in enumerate(b[1:]):
                p = NaiveBayesClassifier.schet(n=data,d=len(words), b1=prisnak[num_4])
                p_massive.append(p)
            b.append(p_massive)
        self.words = words


    def predict(self, X):
        massive_priznak = []

        for num_5, c in enumerate(X):
            slova_razdel = c.split()
            dfgh = []
            ver_massive = self.aprior_massive
            for u, i in enumerate(slova_razdel):
                for t in self.words:
                    if t[0] == i:
                        dfgh.append(t[-1])
                    else:
                        dfgh.append([0 for i in self.s])
            for i in dfgh:
                for num,j in enumerate(i):
                    if j:
                        ver_massive[num]+=math.log10(j)
                    else:
                        ver_massive[num] += 0
            predict_label = max(ver_massive)
            ind = ver_massive.index(predict_label)
            metka = self.index_priznak[ind]
            massive_priznak.append(metka)
        return massive_priznak


    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        pass

    @staticmethod
    def schet(b1, n, d, a=1):
        return (b1 + 1) / (n + a * d)


a = NaiveBayesClassifier()
a.fit(["i love beer", 'hate job','fuck job','bad job'], ["positive", "maybe", 'maybe', 'maybe'])
result = a.predict(['job',"i"])

# TODO import math; math.log()
