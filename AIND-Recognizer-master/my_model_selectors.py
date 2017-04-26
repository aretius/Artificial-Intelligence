import math
import statistics
import warnings
import traceback
import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Baysian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores
        BIC = float('inf')
        best_model= self.base_model(self.n_constant)
        for num_state in range(self.min_n_components, self.max_n_components+1):
            try:
                model = self.base_model(num_state)
                params = model.n_components*model.n_components + 2*model.n_features*(len(self.X[0])) - 1
                logL = model.score(self.X, self.lengths)
                continue
            bic_score = -2 * logL + params*np.log(len(self.X[0]))
            if bic_score < BIC:
                BIC = bic_score
                best_model = model

        return best_model
        # raise NotImplementedError


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores
        max_DIC = -(10**10+10)
        best_model = None
        for i in range(self.min_n_components,self.max_n_components+1):                   
            try:
                model =  self.base_model(i)
            except:
                continue
            try:
                curr_word_score = model.score(self.X,self.lengths)
            except:
                continue
            other_words_score = 0
            for word in self.words:
                if word != self.this_word:
                    otherX,other_lengths = self.hwords[word]
                    try:
                        other_words_score = other_words_score+ model.score(otherX,other_lengths)
                    except:
                        continue
            DIC = curr_word_score - (1/(len(self.words)-1))*other_words_score

            if max_DIC < DIC:
                max_DIC = DIC
                best_model = model

        return best_model
        # raise NotImplementedError


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):

        # TODO implement model selection using CV
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        max_avg_logL = -(10**10+10)
        best_model = None
        n_splits = min(7,len(self.sequences))
        if n_splits == 1:
            return self.base_model(self.n_constant)
        split_method = KFold(n_splits,shuffle = True, random_state=self.random_state)

        for i in range(self.min_n_components,self.max_n_components+1):
            temp_sum_logL = 0.0
            temp_model = self.base_model(i)
            for cv_train_idx,cv_test_idx in split_method.split(self.sequences):

                X_train, lengths_train = combine_sequences(cv_train_idx,self.sequences)
                X_test , lengths_test = combine_sequences(cv_test_idx,self.sequences)
                try:
                    model =  GaussianHMM(n_components=i, covariance_type="diag", n_iter=1000,
                                random_state=self.random_state, verbose=False).fit(X_train,lengths_train)
                except:
                    continue
                try:
                    logL = model.score(X_test,lengths_test)
                except:
                    continue
                temp_sum_logL = temp_sum_logL+logL

            if max_avg_logL< temp_sum_logL/:
                max_avg_logL = temp_sum_logL
                best_model = temp_model

        return best_model
        # raise NotImplementedError