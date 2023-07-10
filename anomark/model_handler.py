import datetime
import pickle
import sys
import time

import numpy as np
import pandas as pd

# custom script for Markov Chains model
from anomark.model import MarkovModel
from anomark.utils.data_handler import apply_modules_to_df
from pandas.errors import ParserError
from tqdm import tqdm

tqdm.pandas()

MARKOV_SCORE = "markovScore"


class MarkovModelHandler:

    @staticmethod
    def run(model_path, data_path, store_bool, col_name, nb_lines=50, color_output=False,
            score_col_name=MARKOV_SCORE, verbose=True, apply_placeholder=False):

        with open(model_path, "rb") as f:
            model: MarkovModel = pickle.load(f)

        df = MarkovModelHandler.load_data(data_path, col_name)
        df[col_name] = df[col_name].astype(str)

        if apply_placeholder:
            print("Applying placeholder transformation...")
            df = apply_modules_to_df(df, col_name)

        result_grouped = MarkovModelHandler.execute_on_df(df, model, col_name, score_col_name)
        threshold = MarkovModelHandler.compute_threshold(model, percent=95)

        # Storing the results in a file if requested
        if store_bool:
            if color_output:
                result_grouped = MarkovModelHandler.add_color_column(result_grouped, model, threshold, col_name)
            MarkovModelHandler.save_execution_results(result_grouped)

        # Displaying results in the terminal
        if verbose:
            MarkovModelHandler.display_top(result_grouped, model, col_name, threshold, nb_lines, color_output)
        return result_grouped

    @staticmethod
    def load_data(path, col_name):
        if path[-4:] == ".csv":
            df = pd.read_csv(path)
        elif path[-4:] == ".txt":
            with open(path, 'r') as f:
                df = f.read()
            df = pd.DataFrame(df.split("\n"), columns=[col_name])
        else:
            try:
                df = pd.read_csv(path)
            except ParserError:
                raise ValueError("The path you provided leads to an unsupported data type. Prefer csv file")
        return df

    @staticmethod
    def colored_results(st: str, model: MarkovModel, threshold: float):
        st = "~" * model.order + st
        res = ""
        begin_token = "\x1b[91m"
        end_token = "\x1b[0m"
        for k in range(model.order, len(st)):
            score = model.log_likelihood(st[k - model.order:k + 1])
            if score < threshold:
                res += begin_token + st[k] + end_token
            else:
                res += st[k]
        res = res.replace(end_token + begin_token, "")
        return res

    @staticmethod
    def execute_on_df(df: pd.DataFrame, model: MarkovModel, col_name, score_col_name=MARKOV_SCORE):
        print("Applying model to dataframe")

        def apply_likelihood(col):
            st = "~" * int(model.order) + str(col)
            return model.log_likelihood(st)
        df[score_col_name] = df[col_name].apply(str).progress_apply(apply_likelihood)

        df_cols = [col for col in list(df.columns) if col != col_name and col != score_col_name]
        grouped_cols = {col: lambda x: ' - '.join(np.unique([str(_) for _ in x]))
                        for col in df_cols}
        grouped_cols.update({score_col_name: min})
        result_grouped = df.groupby(col_name) \
            .agg(grouped_cols) \
            .reset_index().sort_values(score_col_name) \
            .rename({_: 'List of all ' + str(_) for _ in df_cols}, axis=1)

        return result_grouped

    @staticmethod
    def compute_threshold(model, percent):
        """
        Returns the percentage of model prior
        :param model: the MarkovModel model
        :param percent: percentage as a float (ex: 95 for 95%, and not 0.95)
        :return:
        """
        return np.log(model.prior) * percent / 100

    @staticmethod
    def display_top(df: pd.DataFrame, model: MarkovModel, col_name, threshold, nb_lines, color):
        print('_______')
        print("Displaying top {}".format(nb_lines))
        df_slice_map = df[[col_name, MARKOV_SCORE]][:nb_lines].to_dict()
        commands = df_slice_map[col_name]
        scores = df_slice_map[MARKOV_SCORE]

        for item, elt in commands.items():
            print('_______')
            if color:
                print(MarkovModelHandler.colored_results(elt, model, threshold))
            else:
                print(elt)

            # Human-readable percentage to reflect proximity of Markov score to threshold where threshold is the
            # "expected" value.
            print(str(round((1 - (scores[item] / threshold)) * 100, 2)) + "%")
        print('_______')

    @staticmethod
    def add_color_column(df: pd.DataFrame, model: MarkovModel, threshold: float, col_name):
        print("Adding color column")
        # Adding a column with color in results
        df["Colored {}".format(col_name)] = df[col_name] \
            .progress_apply(lambda x: MarkovModelHandler.colored_results(x, model, threshold))
        return df

    @staticmethod
    def save_execution_results(df: pd.DataFrame):
        print("Saving results...")
        now = datetime.datetime.fromtimestamp(time.time())
        output_path = sys.path[0] + '/results/' + now.strftime("%Y%m%d_%Hh%M_") + 'export.csv'
        # save the model to disk
        df.to_csv(output_path, index=False)
        print("Successfully saved results in: {}".format(output_path))

    @staticmethod
    def train_from_df(df: pd.DataFrame, model_order, train_col_name, count_col_name=None, save_model=True,
                      save_path=None, model=None):
        # Preprocessing text data by adding padding to get a complete scan
        df[train_col_name] = df[train_col_name].apply(lambda x: '~' * model_order + str(x) + '~' * model_order)
        # If there is no count column then each occurrence is set to 1
        if not count_col_name:
            count_col_name = "count_col"
            df[count_col_name] = 1

        if not model:
            # Initiating model if none given
            model = MarkovModel(model_order)

        # Training phase
        t0 = time.time()
        df.progress_apply(lambda x: model.train(training_data=x[train_col_name], count=x[count_col_name]), axis=1)
        print("Training took {:.2f} minutes".format((time.time() - t0) / 60))

        # Saving model if asked to
        if save_model:
            MarkovModelHandler.save_model(model=model, save_path=save_path)

        return model

    @staticmethod
    def train_from_txt(training_data, model_order, save_model=True, save_path=None, model=None):
        if not model:
            # Initiating model if no model given
            model = MarkovModel(model_order)

        # Training phase
        t0 = time.time()
        model.train(training_data=training_data)
        print("Training took {:.2f} minutes".format((time.time() - t0) / 60))

        # Saving model if asked to
        if save_model:
            MarkovModelHandler.save_model(model=model, save_path=save_path)

        return model

    @staticmethod
    def save_model(model: MarkovModel, save_path=None):
        # Saving model in pickle format
        print("Saving model...")
        now = datetime.datetime.fromtimestamp(time.time())

        if not save_path:
            save_path = sys.path[0] + '/models/' + now.strftime("%Y%m%d_%Hh%M_") + \
                          'modelLetters_{}grams.dump'.format(model.order)

        with open(save_path, "wb") as output:
            pickle.dump(model, output, protocol=4)
        print("Successfully saved model in: {}".format(save_path))
