# AnoMark

*Anomalies dans des lignes de commande à l'aide de chaînes de Markov*

*Anomaly detection in command lines with Markov chains*

## Motivation

This algorithm is a Machine Learning one, using Natural Language Processing (NLP) techniques based on Markov Chains
and n-grams. It offers a way to train a theoretical model on command lines datasets considered clean. Once done it
can detect malicious command lines on other datasets.

## Technologies used

This package uses standards Data Science Python libraries.

![Generic badge](https://img.shields.io/badge/Python-3.9-blue.svg) ![Made with Jupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?logo=Jupyter)

For ease of installation, it is recommended to use AnoMark after installing Python, conda, and Jupyter Notebooks, with
Anaconda.

<a href='https://www.anaconda.com/products/individual'><img src='https://assets.anaconda.com/production/anaconda-meta.jpg?w=1200&h=630&q=82&auto=format&fit=clip&dm=1632326952&s=2b336a00fa13405f84ce2f5b74e21fee' alt='Anaconda' width=200></img></a>

## Installation

It is recommended to use the conda package manager.

```bash
conda create --name anomark
conda activate anomark
```

The package has only been tested for Python versions >= 3.9.

```bash
conda install python=3.9
```

Required packages can be found in *requirements.txt* file.

```bash
pip install -r requirements.txt
```


## Project structure

<pre>
anomark/
├── anomark-splunk/
   ├── anomark/
   │  ├── ...
   └── README.md
├── apply_model.py
├── csv_data_to_txt.py
├── README_FR.md
├── README.md
├── requirements.txt
├── train_from_csv.py
├── train_from_txt.py
├── data/
    ├── <i>some_training_data.txt</i>
    └── <i>some_data_for_execution.csv</i>
├── models/
    └── <i>some_model.dump</i>
├── notebooks/
   └── Browse_results.ipynb
├── results/
    └── <i>some_result.csv</i>
├── anomark/
   ├── model_handler.py
   ├── model.py
   └── utils/
│     └── data_handler.py
└── tests/
   ├── sample_data
   │  ├── test_data.csv
   │  ├── train_data.csv
   │  └── train_data.txt
   ├── test_data_handler.py
   └── test_model_handler.py
</pre>

Files with names in italic are here as an indication. They will be created during code execution.

## Usage: Training a model

With this code, you can build and execute models. It allows training data creation as well as results exploration.

### Prerequisites

We consider that we start with a dataset in CSV format, containing a column with command lines data, or with a TXT file
with some text in it.

*__N.B.:__ We will use the term 'order' to refer to the number of letters the model might consider in the n-grams construction for
the training part.*

### 1<sup>st</sup> option: Training from _CSV_ data

If your data is stored in a CSV file you may use the `train_from_csv.py` script. It generates a model,
and stores it in the *./models* folder of the project, prepending the name with
the date and hour of creation. There are 3 mandatory flags to use it:

```bash
python train_from_csv.py -d DATA_PATH.csv -o ORDER(int) -c COLUMN_NAME
```

We also supply some flags to train on a defined number of lines from the CSV input. It can be useful
when you have all your data (train and test) in the same CSV. The possible options are listed with the
help flag *-h*. Here is an example for execution:

```bash
python train_from_csv.py -d data/train_data.csv -o 4 -c CommandLine -n 1000 --randomize
```

Usually, we will slice a part of the dataset to create a training part from a time-period defined part
of the data. We can randomize the selection with the `-r` flag, and/or indicate the percentage of lines we want to keep
with `-p`.

*__N.B.:__ When your data is big you can aggregate each sentence by the number of occurrences and define
a count column in your dataframe. Then you supply the count column name to the training script to
reduce the required RAM.*

### 2<sup>nd</sup> option: Training from _TXT_ data

If your data is stored in a TXT file you may use the `train_from_txt.py` script. It generates a model,
and stores it in the *./models* folder of the project, prepending the name with
the date and hour of creation. There are 2 mandatory fields to use it:

```bash
python train_from_txt.py -d DATA_PATH.txt -o ORDER(int)
```


### Resume and output flags

In both cases, you can use two more flags: `--output` and `--resume`. The first one is quite explicit,
it allows you to specify a custom path and name for your model. The second one allows you to start from an existing
model and resume training. To specify the path of the existing model you use the `--model` flag.

### Placeholder flag

You can use the `--placeholder` flag if you want to train a model without considering the GUID, SID,
usernames, and hashes. In the four cases, we replace them with a placeholder after a detection using the following regular
expressions:


| Module | Regex                                                             | Placeholder |
|--------|-------------------------------------------------------------------|-------------|
| GUID   | `\{?[0-9A-Fa-f]{8}[-–]([0-9A-Fa-f]{4}[-–]){3}[0-9A-Fa-f]{12}\}?` | `<GUID>`    |
| SID    | `S[-–]1[-–]([0-9]+[-–])+[0-9]+`                                  | `<SID>`     |
| User   | `(C:\\Users)\\[^\\]*\\`                                          | `<USER>`    |
| Hash   | `\b(?:[A-Fa-f0-9]{64}\|[A-Fa-f0-9]{40}\|[A-Fa-f0-9]{32}\|[A-Fa-f0-9]{20})\b`| `<HASH>`    |

It is a useful flag for reducing the number of false positives. You can edit the regular expressions in
the `anomark/utils/data_handler.py` file.


### Filepath Placeholder flag

You can use the `--filepath-placeholder` flag if you want to train a model without considering the filepath. We replace the filepath with a placeholder after a detection using the following regular
expressions:


| Module | Regex                                                             | Placeholder |
|--------|-------------------------------------------------------------------|-------------|
 | Filepath   | `(?P<opening>\b(?P<montage>[a-zA-Z]:[\/\\])\|[\/\\][\/\\](?<!http:\/\/)(?<!https:\/\/)(?:>[?.][\/\\](?:[^\/\\<>:\"\|?\n\r ]+[\/\\])?(?P=montage)?\|(?!(?P=montage)))\|%\w+%[\/\\]?)(?:[^\/\\<>:\"\|?\n\r ,'][^\/\\<>:\"\|?\n\r]*(?<![ ,'])[\/\\])*(?:(?=[^\/\\<>:\"'\|?\n\r;, ])(?:(?:[^\/\\<>:\"\|?\n\r;, .](?: (?=[\w\-]))?(?:\*(?!= ))?(?!(?P=montage)))+)?(?:\.\w+)*)\|(?:'(?P=opening)(?=.*'\W\|.*'$)(?:[^\/\\<>:'\"\|?\n\r]+(?:'(?=\w))?[\/\\]?)*')\|\"(?P=opening)(?=.*\")(?:[^\/\\<>:\"\|?\n\r]+[\/\\]?)*\"` | `<FILEPATH>`    |

It is a useful flag for reducing the number of false positives **BUT CAN HAVE CONSEQUENCES REGARDING TRUE POSITIVES**. I recommend that you only use this flag if you are dealing with a dataset consisting of command lines from many users who have varied setups and run pretty much any file from any directory under the sun. You can edit the regular expression in
the `anomark/utils/data_handler.py` file.

## Usage: Execution of a model on a dataset

As for the execution phase, the use is similar to the training phase.
We give the model's location with the `-m` flag, the dataset path (*CSV* format) with flag `-d`, and the
column name if different with flag `-c`.

```bash
python apply_model.py -m models/some_model.dump -d data/some_data_for_execution.csv -c COLUMN_NAME
```


By default, the code works on the data supplied and displays the results in the shell of the 50 most unusual
lines according to the model, **grouped** by unique values.

Several more options are available to further the analysis:

- **Recommended:** we can store the results with the `-s` flag. It will create a result file in CSV format containing several columns: command line, some columns which concatenate the unique values for the other variables provided in the dataset for the same command line (for instance every user concerned, or computers), the model's scoring, and the command lines colored (we will give more information on this point later). The generated file is stored in the *./results* folder with a name prepended with the date and hour of creation. We will be able to explore the file with the *Browse_results.ipynb* notebook.
- we can transform our testing data with placeholders, similarly to the training phase with the `--placeholder` flag.
- we can color the results in the shell with the `--color` flag. The most unusual letters are displayed in red, as to enhance our comprehension of how the model judges a command line as unusual.
- we can enable the silent mode in the shell with the `--silent` flag.
- we can choose the number of lines displayed in the shell with the `-n` flag.

*__N.B.:__ It is recommended to use the store flag (`-s`) as soon as we want to dive a bit more into the results,
for instance using a notebook.*

## Results exploration with notebooks

You will find the notebooks in the *./notebooks* folder of the project.
It is necessary to launch either *jupyter-noteboook* or *jupyter-lab* from a parent folder
(to access the results files). Jupyter should be installed simultaneously with the Anaconda suite,
and you can launch it from the shell (or from the Anaconda navigator). It can also be installed without the
Anaconda suite.

Instructions are detailed inside the notebooks.

## Presentations
* [FRENCH] JUNIUS, Alexandre. ["AnoMark - Détection d’Anomalies dans des lignes de commande à l’aide de Chaînes de Markov."](https://www.sstic.org/2022/presentation/anomark_detection_anomalies_dans_des_lignes_de_commande_chaines_de_markov/), SSTIC 2022 (Symposium sur la sécurité des technologies de l'information et des communications).
* [ENGLISH] JUNIUS, Alexandre. ["Anomark - Anomaly Detection in Command Lines with Markov Chains"](https://www.youtube.com/watch?v=RACIZZMzI9I), 35th Annual FIRST conference, 2023.
