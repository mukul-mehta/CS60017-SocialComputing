import spacy
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.svm import SVC


def svmModel(train_data, test_data, validation=False, validation_size=0.15, download_pretrained=False):
    if download_pretrained:
        spacy.cli.download('en_core_web_md')
    nlp = spacy.load('en_core_web_md')

    embeddings = [nlp(text['tweet']).vector for text in train_data]
    labels = [text['label'] for text in train_data]

    if validation:
        embeddings_train, embeddings_validation, labels_train, labels_validation = train_test_split(
            embeddings, labels, test_size=validation_size)
    else:
        embeddings_train, labels_train = embeddings, labels

    svmClassifier = SVC()
    svmClassifier.fit(embeddings_train, labels_train)
    accuracy = None
    f1_macro = None

    if validation:
        y_pred = svmClassifier.predict(embeddings_validation)
        accuracy = metrics.accuracy_score(labels_validation, y_pred)
        f1_macro = metrics.f1_score(labels_validation, y_pred, average="macro")

        svmClassifier.fit(embeddings, labels)

    results = []
    test_embeddings = [nlp(text['tweet']).vector for text in test_data]
    y_pred = svmClassifier.predict(test_embeddings)

    for i, tweet in enumerate(test_data):
        t = {
            'id': tweet['id'],
            'tweet': tweet['tweet'],
            'label': y_pred[i]
        }
        results.append(t)

    return results, accuracy, f1_macro
