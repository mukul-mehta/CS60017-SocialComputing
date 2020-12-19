import fasttext
import os

from sklearn.model_selection import train_test_split
from sklearn import metrics


def FastTextModel(train_data, test_data, pretrained_model_path, validation=True, validation_size=0.15, lr=0.1, epochs=25, use_downloaded=False):
    accuracy = None
    f1_score = None

    if (not os.path.exists(pretrained_model_path)) or (not use_downloaded):
        ft_data = [
            f"__label__{row['label']} {row['tweet']}" for row in train_data]
        labels = [row['label'] for row in train_data]

        if validation:
            data_train, data_validation, labels_train, labels_validation = train_test_split(
                ft_data, labels, test_size=validation_size)
        else:
            data_train, labels_train = ft_data, labels

        with open("fasttext.train", "w") as f:
            for i in data_train:
                f.write(i)
                f.write("\n")

        model = fasttext.train_supervised(
            input="fasttext.train", epoch=epochs, lr=lr)

        model.save_model(pretrained_model_path)

        if validation:
            y_pred = []
            for i in data_validation:
                sentence = ' '.join(i.split()[1:])
                label = int(model.predict(sentence)[
                    0][0].replace("__label__", ""))
                y_pred.append(label)

            accuracy = metrics.accuracy_score(labels_validation, y_pred)
            f1_score = metrics.f1_score(
                labels_validation, y_pred, average="macro")

            with open("fasttext.train", "w") as f:
                for i in ft_data:
                    f.write(i)
                    f.write("\n")

            model = fasttext.train_supervised(
                input="fasttext.train", epoch=epochs, lr=lr)
            model.save_model(pretrained_model_path)

    else:
        model = fasttext.load_model(pretrained_model_path)

    test_documents = [row['tweet'] for row in test_data]
    y_pred = [int(model.predict(document)[0][0].replace("__label__", ""))
              for document in test_documents]

    results = []
    for i, tweet in enumerate(test_data):
        t = {
            'id': tweet['id'],
            'tweet': tweet['tweet'],
            'label': y_pred[i]
        }
        results.append(t)

    return results, accuracy, f1_score
