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
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    all_sequences = test_set.get_all_sequences()
    all_Xlengths = test_set.get_all_Xlengths()
    for i, _ in all_sequences.items():
        X, lengths = test_set.get_item_Xlengths(i)
        selected_model_score = float('-inf')
        selected_word = None
        model_world_dict = {}
        for model_dict_id in models.keys():
            model = models[model_dict_id]
            model_world_dict[model_dict_id] = 0
            try:
                logL = model.score(X, lengths)
                model_world_dict[model_dict_id] = logL
                if logL > selected_model_score:
                    selected_word = model_dict_id
                    selected_model_score = logL
            except:
                pass
        probabilities.append(model_world_dict)
        guesses.append(selected_word)
        
    return probabilities,guesses   

