from math import log
from random import choice, random


def normalize_transition_matrix(matrix: dict):
    """
    Normalize the transition counts into a proper transition matrix.
    """
    output = {}
    for (substr, dictionary) in list(matrix.items()):
        total = sum(dictionary.values())
        output[substr] = {key: dictionary[key] / float(total) for key in list(dictionary.keys())}
    return output


class MarkovModel:

    def __init__(self, order):
        self.order = order
        self.markov_chain = {}
        self.normed_chain = {}
        self.prior = .001
        self.alphabet = []

    def train(self, training_data=None, count=1):
        """
        Parse input data to update Markov transition matrix. Could be called multiple times.
        """

        # Update transition matrix
        for i in range(len(training_data) - self.order):
            current_ngram = training_data[i: i + self.order]
            next_letter = training_data[i + self.order]

            self.markov_chain[current_ngram] = self.markov_chain.get(current_ngram, {})
            self.markov_chain[current_ngram][next_letter] = self.markov_chain[current_ngram].get(next_letter, 0) + count
            if next_letter not in self.alphabet:
                self.alphabet.append(next_letter)

    def normalize_model_and_compute_prior(self):
        self.normed_chain = normalize_transition_matrix(self.markov_chain)
        self.alphabet = sorted(self.alphabet)
        # Computing the minimum probability as the prior of the model
        probabilities = [v for d in self.normed_chain.values() for v in d.values()]
        self.prior = .01 * min(probabilities)

    def simulate(self, length, start=None):
        """
        Generate a new sequence drawn from the trained Markov model.

        Args:
            length (int): The length of the sequence to be produced
            start (str): A starting portion of text for the simulation
                         to begin with
        Returns:
            (str): A simulated sequence of the proscribed length,
                     drawn from the trained Markov model
        """
        self.check_if_trained()

        if start is None:
            simulation = choice(list(self.normed_chain.keys()))
        else:
            simulation = start
        length = max(0, length - len(simulation))

        # Random walk simulation
        for i in range(length):
            ngram = simulation[-self.order:]
            simulation += self.generate_letter(ngram)
        return simulation

    def generate_letter(self, ngram):
        """ Return a random letter from a ngram.  """
        self.check_if_trained()

        if ngram in self.normed_chain.keys():
            distribution = self.normed_chain[ngram]
            r = random()
            for (key, num) in list(distribution.items()):
                r -= num
                if r <= 0:
                    return key
        else:
            return choice(self.alphabet)

    def log_likelihood(self, sequence):
        """
        Compute the log likelihood of a test sequence given the trained Markov model.

        Args:
            sequence (str): A sequence of interest
        Returns:
            (float): The computed average log likliehood of the sequence.
        """
        self.check_if_trained()

        log_likelihoods = []

        # Compute log likelihoods for each transition in the test sequence
        for i in range(len(sequence) - self.order):
            ngram, next_letter = sequence[i: i + self.order], sequence[i + self.order]
            # Retrieving probability from existing trained model, or getting prior
            distribution = self.normed_chain.get(ngram, {})
            probability = distribution.get(next_letter, self.prior)
            log_likelihoods.append(log(probability))

        if not log_likelihoods:
            return log(self.prior)
        # Averaging log likelihoods
        return 1 / float(len(log_likelihoods)) * sum(log_likelihoods)

    def check_if_trained(self):
        if not self.normed_chain:
            if not self.markov_chain:
                raise ValueError("Must train model before simulating new sequences")
            else:
                self.normalize_model_and_compute_prior()
        else:
            return True
