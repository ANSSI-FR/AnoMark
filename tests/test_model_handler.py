from unittest import TestCase

import pandas as pd
from anomark.model_handler import MarkovModelHandler as mmh


class Test(TestCase):
    def test_train_on_txt(self):
        with open("tests/sample_data/train_data.txt", "r") as f:
            text_data = f.read()
        model = mmh.train_from_txt(training_data=text_data, model_order=4, save_model=False)

        expected_markov_chain = {'This': {' ': 6}, 'his ': {'i': 6}, 'is i': {'s': 6}, 's is': {' ': 6},
                                 ' is ': {'s': 6, 'd': 1}, 'is s': {'o': 6}, 's so': {'m': 6}, ' som': {'e': 6},
                                 'some': {' ': 6}, 'ome ': {'d': 6, 'n': 1}, 'me d': {'a': 6}, 'e da': {'t': 6},
                                 ' dat': {'a': 7}, 'data': {'~': 6}, 'ata~': {'~': 6}, 'ta~~': {'~': 6},
                                 'a~~~': {'~': 6}, '~~~~': {'T': 5, 'S': 1}, '~~~T': {'h': 5}, '~~Th': {'i': 5},
                                 '~Thi': {'s': 5}, '~~~S': {'o': 1}, '~~So': {'m': 1}, '~Som': {'e': 1},
                                 'Some': {' ': 1}, 'me n': {'e': 1}, 'e ne': {'w': 1}, ' new': {' ': 1},
                                 'new ': {'i': 1}, 'ew i': {'s': 1}, 'w is': {' ': 1}, 'is d': {'a': 1},
                                 's da': {'t': 1}}

        self.assertEqual(expected_markov_chain, model.markov_chain)
        self.assertEqual(4, model.order)
        self.assertEqual(0.001, model.prior)

    def test_train_on_csv(self):
        df = pd.read_csv("tests/sample_data/train_data.csv").iloc[:3]
        model = mmh.train_from_df(df=df, model_order=4, train_col_name="column1", count_col_name="count",
                                  save_model=False)

        expected_markov_chain = {'~~~~': {'T': 10, 'S': 3, 'w': 1}, '~~~T': {'h': 10}, '~~Th': {'i': 10},
                                 '~Thi': {'s': 10}, 'This': {' ': 10}, 'his ': {'i': 10}, 'is i': {'s': 10},
                                 's is': {' ': 10}, ' is ': {'s': 10, 'd': 3}, 'is s': {'o': 10}, 's so': {'m': 10},
                                 ' som': {'e': 10}, 'some': {' ': 10}, 'ome ': {'d': 10, 'n': 3}, 'me d': {'a': 10},
                                 'e da': {'t': 10}, ' dat': {'a': 13}, 'data': {'~': 13}, 'ata~': {'~': 13},
                                 'ta~~': {'~': 13}, 'a~~~': {'~': 13}, '~~~S': {'o': 3}, '~~So': {'m': 3},
                                 '~Som': {'e': 3}, 'Some': {' ': 3}, 'me n': {'e': 3}, 'e ne': {'w': 3},
                                 ' new': {' ': 3}, 'new ': {'i': 3}, 'ew i': {'s': 3}, 'w is': {' ': 3},
                                 'is d': {'a': 3}, 's da': {'t': 3}, '~~~w': {'o': 1}, '~~wo': {'r': 1},
                                 '~wor': {'d': 1}, 'word': {'~': 1}, 'ord~': {'~': 1}, 'rd~~': {'~': 1},
                                 'd~~~': {'~': 1}}

        self.assertEqual(expected_markov_chain, model.markov_chain)
        self.assertEqual(4, model.order)
        self.assertEqual(0.001, model.prior)
