import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    # TODO implement the recognizer

    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    for i in range(test_set.num_items):
        top_prob, top_word = float("-inf"), None
        word_prob = {}
        seq, length = test_set.get_item_Xlengths(i)
        for word, model in models.items():
            try:
                word_prob[word] = model.score(seq, length)
            except Exception as e:
                word_prob[word] = float("-inf")
            if word_prob[word] > top_prob:
                top_prob, top_word = word_prob[word], word

        probabilities.append(word_prob)
        guesses.append(top_word)

    return probabilities, guesses

    # return probabilities, guesses


