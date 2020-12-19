#####################################
#### Mukul Mehta | 18CS10033     ####
#### CS60017 -> Social Computing ####
#### Programming Assignment 3    ####
#####################################


import csv
import os

from models.random_forest import randomForestModel
from models.svm import svmModel
from models.fasttext import FastTextModel
from utils import preprocessTweets, read_config


# Dictionary of locations of data and prediction
PATHS = read_config(filename="config.ini", section="PATHS")


def writeResults(filename, data):
    """
    Write Results to files in the appropriate folders

    Parameters
    ----------
    filename: (str)
        Name of the file the predictions are written to
    data: (list)
        List of predictions from the models. Each entry is a dictionary with
        3 fields: "id", "text" and "label". We only write the IDs and predicted labels to disk
    ----------
    """

    f = open(os.path.join(PATHS["PREDICTIONS_PATH"], filename), "w")

    fieldnames = ["id", "hateful"]
    writer = csv.writer(f, )
    writer.writerow(fieldnames)

    for tweet in data:
        row = [tweet['id'], tweet['label']]
        writer.writerow(row)


def runRandomForest(train_data, test_data):
    """
    Run the Random Forest model on TF-IDF vectors and predict labels on test data

    Parameters
    ----------
    train_data: (list)
        Preprocessed Training Data
    test_data: (list)
        Preprocessed Test Data (IDs and Text)
    ----------

    Returns
    ----------
    results: (list)
    accuracy: (float)
    f1_score: (float)
    ----------
    """
    RF = read_config(filename="config.ini", section="RANDOM_FOREST")
    results, accuracy, f1_score = randomForestModel(train_data, test_data, validation=bool(
        RF["VALIDATION"]), validation_size=float(RF["VALIDATION_SIZE"]),
        n_estimators=int(RF["N_ESTIMATORS"]), min_df=int(RF["MIN_DF"]), max_df=float(RF["MAX_DF"]))

    writeResults(PATHS["RF_FILE"], results)
    return results, accuracy, f1_score


def runSVM(train_data, test_data):
    """
    Run the SVM model on SpaCy embeddings and predict labels on test data

    Parameters
    ----------
    train_data: (list)
        Preprocessed Training Data
    test_data: (list)
        Preprocessed Test Data (IDs and Text)
    ----------

    Returns
    ----------
    results: (list)
    accuracy: (float)
    f1_score: (float)
    ----------
    """
    SVM = read_config(filename="config.ini", section="SVM")
    results, accuracy, f1_score = svmModel(train_data, test_data, validation=bool(
        SVM["VALIDATION"]), validation_size=float(SVM["VALIDATION_SIZE"]), download_pretrained=bool(SVM["DOWNLOAD_PRETRAINED_SPACY"]))

    writeResults(PATHS["SVM_FILE"], results)
    return results, accuracy, f1_score


def runFastText(train_data, test_data):
    """
    Run the FastText model and predict labels on test data

    Parameters
    ----------
    train_data: (list)
        Preprocessed Training Data
    test_data: (list)
        Preprocessed Test Data (IDs and Text)
    ----------

    Returns
    ----------
    results: (list)
    accuracy: (float)
    f1_score: (float)
    ----------
    """
    FT = read_config(filename="config.ini", section="FASTTEXT")
    results, accuracy, f1_score = FastTextModel(train_data, test_data, pretrained_model_path=FT["FASTTEXT_MODEL_PATH"], validation=bool(
        FT["VALIDATION"]), validation_size=float(FT["VALIDATION_SIZE"]), lr=float(FT["LR"]), epochs=int(
        FT["EPOCHS"]), use_downloaded=FT["USE_DOWNLOADED"])

    writeResults(PATHS["FT_FILE"], results)
    return results, accuracy, f1_score


if __name__ == "__main__":
    DATA_PATH = PATHS["DATA_PATH"]
    TRAIN_FILE = PATHS["TRAIN_FILE"]
    TEST_FILE = PATHS["TEST_FILE"]

    raw_train_data = []
    raw_test_data = []

    # Load the Raw Train and Test data

    with open(os.path.join(DATA_PATH, TRAIN_FILE)) as f:
        reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
        next(reader, None)

        for row in reader:
            _row = [int(row[0]), row[1], int(row[2])]
            raw_train_data.append(_row)

    with open(os.path.join(DATA_PATH, TEST_FILE)) as f:
        reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
        next(reader, None)

        for row in reader:
            _row = [int(row[0]), row[1]]
            raw_test_data.append(_row)

    # Preprocess tweets and save them to disk for using as model inputs
    train_data, test_data = preprocessTweets(
        raw_train_data=raw_train_data, raw_test_data=raw_test_data)

    PROCESSED_DATA_PATH = PATHS["PROCESSED_DATA_PATH"]

    with open(os.path.join(PROCESSED_DATA_PATH, TRAIN_FILE), "w") as f:
        writer = csv.writer(f, delimiter="\t")
        for row in train_data:
            writer.writerow(row)

    with open(os.path.join(PROCESSED_DATA_PATH, TEST_FILE), "w") as f:
        writer = csv.writer(f, delimiter="\t")
        for row in test_data:
            writer.writerow(row)

    STATS = {}

    # print("Running Random Forest with TF-IDF vectors")
    results, accuracy, f1_score = runRandomForest(train_data, test_data)
    STATS["RF"] = {
        "accuracy": accuracy,
        "f1_score": f1_score
    }
    # print(f"Accuracy -> {accuracy}  |  F1 Macro Score -> {f1_score}\n")

    # print("Running SVM with Word2Vec pretrained embeddings from SpaCy")
    results, accuracy, f1_score = runSVM(train_data, test_data)
    STATS["SVM"] = {
        "accuracy": accuracy,
        "f1_score": f1_score
    }
    # print(f"Accuracy -> {accuracy}  |  F1 Macro Score -> {f1_score}\n")

    # print("Running Fasttext trained on our dataset")
    results, accuracy, f1_score = runFastText(train_data, test_data)
    STATS["FT"] = {
        "accuracy": accuracy,
        "f1_score": f1_score
    }
    # print(f"Accuracy -> {accuracy}  |  F1 Macro Score -> {f1_score}\n")
