from math import log
from math import exp
import numpy as np

class TextClassifier:
    """
    In this question, you will implement a classifier that predicts
    the number of stars a reviewer gave a movie from the text of the review.

    You will process the reviews in the dataset we provide, then
    implement a Naive Bayes classifier to do the prediction.

    But first, some math!
    """

    def q0(self):
        """
        Return your full name as it appears in the class roster as well as all collaborators as a list of strings
        """
        return ["Bennett Parsons", "Yankang Yang"]

    def q1(self):
        """
        Suppose you roll a 4-sided die of unknown bias, and you observe
        the following sequence of values:
        3   1   4   4   2   1   2   4   2   1   2   1   1   1   1   4   3   4   4   1
        Given only this information, what are the most likely
        probabilities of rolling each side? (Hardcoding is fine)
        """
        vals = [3, 1, 4, 4, 2, 1, 2, 4, 2, 1, 2, 1, 1, 1, 1, 4, 3, 4, 4, 1]
        counts = [sum([1.0 for j in vals if (i+1) == j]) for i in range(4)]
        normalized = [i/len(vals) for i in counts]
        return normalized

    def q2(self):
        """
        You just fit a multinomial distribution!

        Now suppose you have a prior belief that the die is fair.
        After some omitted math involving a conjugate Dirichlet distribution,
        you realize that you can encode this prior by simply adding
        some "fake" observations of each side. The number of observations
        is the "strength" of your prior belief.
        Using the same observations as in q1 and a prior with a per-side
        "strength" of 2, what are the probabilities of rolling each side??
        """
        # just add 2 of each side to vals list from before
        vals = [1, 1, 2, 2, 3, 3, 4, 4, 3, 1, 4, 4, 2, 1, 2, 4, 2, 1, 2, 1, 1, 1, 1, 4, 3, 4, 4, 1]
        counts = [sum([1.0 for j in vals if (i+1) == j]) for i in range(4)]
        normalized = [i/len(vals) for i in counts]
        return normalized

    def q3(self, counts=[1,1,3,8]):
        """
        You might be wondering what dice have to do with NLP.
        We will model each possible rating (one of the five numbers of stars)
        as a die, with each word in the dictionary as a face.

        This is a multinomial Naive Bayes classifier, because the words are
        drawn from a per-rating multinomial distribution and we treat
        each word in a review as independent (conditioned on the rating). That is,
        once the rating has emitted one word to the review, the next word
        has the same distribution over possible values as the first.

        In this question, you will write a function that computes p(word|rating), the
        probability that the rating under question will produce
        each of the four words in our dictionary. We will run this function
        5 times, once for each rating. We pass in the number of times each
        word shows up in any review corresponding to the current rating.
        """
        s = sum(counts)
        return [(i*1.0)/s for i in counts]

    def q4(self, infile):
        """
        You'll notice that actual words didn't appear in the last question.
        Array indices are nicer to work with than words, so we typically
        write a dictionary encoding the words as numbers. This turns
        review strings into lists of integers. You will count the occurrences
        of each integer in reviews of each class.

        The infile has one review per line, starting with the rating and then a space.
        Note that the "words" include things like punctuation and numbers. Don't worry
        about this distinction for now; any string that occurs between spaces is a word.

        You must do three things in this question: build the dictionary,
        count the occurrences of each word in each rating and count the number
        of reviews with each rating.
        The words should be numbered sequentially in the order they first appear.
        counts[ranking][word] is the number of times word appears in any of the
        reviews corresponding to ranking
        nrated[ranking] is the total number of reviews with each ranking
        """
        word_count = 0
        self.dict = {}
        self.counts = [[] for _ in range(5)]
        self.nrated = [0]*5
        self.words = []       # self.dict[self.words[x]] == x
        with open(infile) as f:
            reviews = f.readlines()
            for review in reviews:
                words = review.split()
                score = int(words[0])    # first word is always the rating
                for word in words[1:]:
                    if word not in self.dict:    # add new words to dict
                        self.dict[word] = word_count
                        word_count += 1
                        self.words.append(word)
                        for i in range(5):       # expand dict as necessary
                            self.counts[i].append(0)
                    assert(len(self.counts[score]) >= word_count)
                    self.counts[score][self.dict[word]] += 1
                self.nrated[score] += 1

    def q5(self, alpha=1):
        """
        Now you'll fit the model. For historical reasons, we'll call it F.
        F[rating][word] is -log(p(word|rating)).
        The ratings run from 0-4 to match array indexing.
        Alpha is the per-word "strength" of the prior (as in q2).
        (What might "fairness" mean here?)
        """
        # add alpha to all counts and normalize, then take -log
        update = [self.q3(counts=[self.counts[score][word] + alpha for word in range(len(self.dict))]) for score in range(5)]
        self.F = [[-log(word_prob) if word_prob != 0 else 0 for word_prob in word_probs] for word_probs in update]


# use self.F from q5

    def q6(self, infile):
        """
        Test time! The infile has the same format as it did before. For each review,
        predict the rating. Ignore words that don't appear in your dictionary.
        Are there any factors that won't affect your prediction?
        You'll report both the list of predicted ratings in order and the accuracy.
        """
        if infile == "stsa.self.test":
            infile = "stsa.test"
        with open(infile) as f:
            reviews = f.readlines()
            predictions = []
            total = 0
            right = 0
            for review in reviews:
                words = review.split()
                actual_score = int(words[0])
                total += 1.0
                counts = [0]*5
                score_prior = self.q3(counts=self.nrated)  # score_prior[x] = P(score=x)
                probs = [score_prior[i] for i in range(5)]
                for score in range(5):
                    for word in words[1:]:
                        if word in self.dict:
                            probs[score] *= exp(-self.F[score][self.dict[word]])
                predict_score = np.array(probs).argmax()   # min because self.F has -log() of P(word|score)
                if predict_score == actual_score:
                    right += 1.0
                predictions.append(predict_score)

        return (predictions, right/total)



# directly calculate probabilities according to @469

    # def q6(self, infile):
    #     """
    #     Test time! The infile has the same format as it did before. For each review,
    #     predict the rating. Ignore words that don't appear in your dictionary.
    #     Are there any factors that won't affect your prediction?
    #     You'll report both the list of predicted ratings in order and the accuracy.
    #     """
    #     if infile == "stsa.self.test":
    #         infile = "stsa.test"
    #     with open(infile) as f:
    #         reviews = f.readlines()
    #         predictions = []
    #         total = 0
    #         right = 0
    #         print "Nice counts!"
    #         for rating in range(5):
    #             print rating, ": ",
    #             for i in range(len(self.counts[rating])):
    #                 word = self.words[i]
    #                 count = self.counts[rating][i]
    #                 if count > 0:
    #                     print (word, count),
    #             print
    #         print
    #         for review in reviews:
    #             words = review.split()
    #             actual_score = int(words[0])
    #             total += 1.0
    #             counts = [0]*5
    #             score_prior = self.q3(counts=self.nrated)
    #             print
    #             print "Review:", review
    #             print "prior:", score_prior
    #             probs = [score_prior[i] for i in range(5)]
    #             for score in range(5):
    #                 for word in words[1:]:
    #                     if word in self.dict:
    #                         probs[score] *= self.q3(counts=self.counts[score])[self.dict[word]]
    #                         # print "After word", word, "probs are:", probs
    #             print "post:", self.q3(counts=probs)
    #             predict_score = np.array(probs).argmax()
    #             if predict_score == actual_score:
    #                 right += 1.0
    #             predictions.append(predict_score)

    #     return (predictions, right/total)




# counting! definitely wrong I think

    # def q6(self, infile):
    #     """
    #     Test time! The infile has the same format as it did before. For each review,
    #     predict the rating. Ignore words that don't appear in your dictionary.
    #     Are there any factors that won't affect your prediction?
    #     You'll report both the list of predicted ratings in order and the accuracy.
    #     """
    #     if infile == "stsa.self.test":
    #         infile = "stsa.test"
    #     with open(infile) as f:
    #         reviews = f.readlines()
    #         predictions = []
    #         total = 0
    #         right = 0
    #         # print "Nice counts!"
    #         # for word in self.dict:
    #         #     print word, ": ",
    #         #     for rating in range(5):
    #         #         print self.counts[rating][self.dict[word]],
    #         #     print
    #         # print
    #         for review in reviews:
    #             words = review.split()
    #             actual_score = int(words[0])
    #             total += 1.0
    #             counts = [0]*5
    #             # print "Review:", review
    #             for word in words[1:]:
    #                 if word in self.dict:
    #                     for score in range(5):
    #                         counts[score] += self.counts[score][self.dict[word]]
    #             # print counts
    #             predict_score = np.array(counts).argmax()
    #             if predict_score == actual_score:
    #                 right += 1.0
    #             predictions.append(predict_score)

    #     # return (predictions, right/total)
    #     return ([4,0,2], 0.3333333)

    def q7(self, infile):
        """
        Alpha (q5) is a hyperparameter of this model - a tunable option that affects
        the values that appear in F. Let's tune it!
        We've split the dataset into 3 parts: the training set you use to fit the model
        the validation and test sets you use to evaluate the model. The training set
        is used to optimize the regular parameters, and the validation set is used to
        optimize the hyperparameters. (Why don't you want to set the hyperparameters
        using the test set accuracy?)
        Find and return a good value of alpha (hint: you will want to call q5 and q6).
        What happens when alpha = 0?
        """
        return 0

    def q8(self):
        """
        We can also "hallucinate" reviews for each rating. They won't make sense
        without a language model (for which you'll have to take CS287), but we can
        list the 3 most representative words for each class. Representative here
        means that the marginal information it provides (the minimal difference between
        F[rating][word] and F[rating'][word] across all rating' != rating) is maximal.
        You'll return the strings rather than the indices, and in decreasing order of
        representativeness.
        """
        return [["182", "compsci", "."] for _ in range(5)]

    """
    You did it! If you're curious, the dataset came from (Socher 2013), which describes
    a much more sophisticated model for this task.
    Socher, R., Perelygin, A., Wu, J. Y., Chuang, J., Manning, C. D., Ng, A. Y., and Potts, C. (2013). Recursive deep models for semantic compositionality over a sentiment treebank. In Proceedings of the conference on empirical methods in natural language processing (EMNLP), volume 1631, page 1642. Citeseer.
    """

if __name__ == '__main__':
    c = TextClassifier()
    print "Processing training set..."
    c.q4('mini.train')
    print len(c.dict), "words in dictionary"
    print "Fitting model..."
    c.q5()
    print "Accuracy on validation set:", c.q6('mini.valid')
    print "Good alpha:", c.q7('mini.valid')
    c.q5() #reset alpha
    print "Happy words:", " and ".join(c.q8()[4][:2])
