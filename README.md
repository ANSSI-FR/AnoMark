# AnoMark

*Anomalies dans des lignes de commande à l'aide de chaînes de Markov*  
*Anomaly detection in command lines with Markov chains*

## Motivation

This algorithm is a Machine Learning one, using Natural Language Processing (NLP) techniques based on Markov Chains
and n-grams. It offers a way to train a theoretical model on command lines datasets considered as clean. Once done it
is able to detect malicious command lines on other datasets.

## Technologies used

This package uses standards Data Science python libraries.

![Generic badge](https://img.shields.io/badge/Python-3.9-blue.svg) ![Made with Jupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?logo=Jupyter)

For ease of installation it is recommend to use AnoMark after installing python, conda, and Jupyter Notebooks, with 
Anaconda.

<a href='https://www.anaconda.com/products/individual'><img src='https://assets.anaconda.com/production/anaconda-meta.jpg?w=1200&h=630&q=82&auto=format&fit=clip&dm=1632326952&s=2b336a00fa13405f84ce2f5b74e21fee' alt='Anaconda' width=200></img></a>

## Installation

It is recommended to use the conda package manager.

```bash
conda create --name anomark
conda activate anomark
```

The package has only been tested for python versions superior or equal to 3.9.

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
├── scripts/
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

Files with name in italic are here as indication. They will be created during code execution.

## Usage: Training a model

With these codes you can build and execute models. It allows training data creation to results exploration.

### Prerequisites

We consider that we start with a dataset in csv format, containing a column with command lines data ; or with a txt file
with some text in it.

*__N.B.:__ We will call order the number of letters the model might consider in the n-grams construction for
the training part.*

### 1<sup>st</sup> option: Training from _csv_ data

If youre data is stored in a CSV file you may use the `train_from_csv.py` script. It generates a model, 
and store it in the *./models* folder of the project, prepending the name with
the date and hour of creation.  There are 3 mandatory flags to use it:

```bash
python train_from_csv.py -d DATA_PATH.csv -o ORDER(int) -c COLUMN_NAME
```

We also provide some flags to train on a defined number of lines from the csv input. It can be useful
when you have all your data (train and test) in the same csv. The possible options are listed with the
help flag *-h*. We give here an execution example :

```bash
python train_from_csv.py -d data/train_data.csv -o 4 -c CommandLine -n 1000 --randomize
```

Usually we will slice a part of the dataset as to create a training part from a time-period defined part 
of the data. We can randomize the selection with the `-r` flag, and/or indicate the percentage of lines we want to keep 
with `-p`.

*__N.B.:__ When your data is big you can aggregate each sentence by the number of occurrences and define
a count column in your dataframe. Then you provide the count column name to the training script as to
reduce the required RAM.*

### 2<sup>nd</sup> option: Training from _txt_ data

If your data is stored in a TXT file you may use the `train_from_txt.py` script. It generates a model, 
and store it in the *./models* folder of the project, prepending the name with
the date and hour of creation. There are 2 mandatory fields to use it:

```bash
python train_from_txt.py -d DATA_PATH.txt -o ORDER(int)
```


### Resume and output flags

In both cases you can use two more flags : `--output` and `--resume`. The first one is quite explicite,
it allows to specify a custom path and name for your model. The second one allows to start from an existing
model and to resume training. As to specify the path of the existing model you may use the `--model` flag.

### Placeholder flag

Eventually you can use the `--placeholder` flag if you want to train a model without considering the GUID, SID, and
usernames. In the three cases, we replace them by a placeholder after a detection using the following regular 
expressions :


| Module | Regex                                                      | Placeholder |
|--------|------------------------------------------------------------|-------------|
 | GUID   | `\{?[0-9A-Fa-f]{8}-([0-9A-Fa-f]{4}-){3}[0-9A-Fa-f]{12}\}?` | `<GUID>`    |
 | SID    | `S-1–([0-9]+-)+[0-9]+`                                     | `<SID>`     |
 | User   | `C:\\Users\\[^\\]*\\`                                      | `<USER>`    |

It is a flag quite useful to reduce the number of false positives. You can edit the regular expressions in
the `scripts/utils/data_handler.py` file.

## Usage: Execution of a model on a dataset

As for the execution phase, the use is very similar to the training phase.
We give: the model's location with `-m` flag, the dataset path (*csv* format) with flag `-d`, and the
column name if different with flag `-c`.

```bash
python apply_model.py -m models/some_model.dump -d data/some_data_for_execution.csv -c COLUMN_NAME
```


By default, the code works on the data provided and displays the results in the shell of the 50 most unusual
lines according to the model, **grouped** by unique values.

Several more options are available to further the analysis :

- **Recommended:** we can store the results with `-s` flag. It will create a result file in csv format containing several columns : command line, some columns which concatenate the unique values for the other variables provided in the dataset for a same command line (for instance every user concerned, or computers), the model's scoring, and the command lines colored (we will give more information on this point later). The generated file is stored in the *./results* folder with a name prepended with the date and hour of creation. We will be able to explore the file with the *Browse_results.ipynb* notebook.
- we can transform our testing data with placeholders, similarly to the training phase with `--placeholder` flag.
- we can color the results in the shell with the `--color` flag. The most unusual letters are displayed in red, as to enhance our comprehension of how the model judges a command line as unusual.
- we can enable the silent mode in the shell with the `--silent` flag.
- we can choose the number of lines displaying in the shell with the `-n` flag.

*__N.B. :__ It is recommended to use the store flag as soon as we want to dive a bit more in the results
for instance using a notebook.*

## Results exploration with notebooks

You will find the notebooks in the *./notebooks* folder of the project.
It is necessary to launch either *jupyter-noteboook* or *jupyter-lab* from a parent folder
(as to access the results files). Jupyter should be installed simultaneously with the Anaconda suite,
and you can launch it from the shell (or from the anaconda navigator). It can also be installed without the
anaconda suite.

Instructions are detailed inside the notebooks.

## Presentations
* [FRENCH] JUNIUS, Alexandre. ["AnoMark - Détection d’Anomalies dans des lignes de commande à l’aide de Chaînes de Markov."](https://www.sstic.org/2022/presentation/anomark_detection_anomalies_dans_des_lignes_de_commande_chaines_de_markov/)   
SSTIC 2022 (Symposium sur la sécurité des technologies de l'information et des communications).
