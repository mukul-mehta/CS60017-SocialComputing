from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from sklearn.model_selection import train_test_split


def randomForestModel(train_data, test_data, validation=False, validation_size=0.15, n_estimators=256, min_df=5, max_df=0.8):
    """
    Generate TF-IDF vectors for the corpus and run the Random Forest model for classification

    Parameters
    ----------
    train_data: ([dict])
        The training examples. Each entry is a dict with 3 keys: "id", "tweet" and "label"
    test_data: ([dict])
        The test set examples. Each entry is a dict with 2 keys: "id" and "tweet"
    validation: (bool, optional), Defaults to False
        Split the training set into a validation set and measure performance
    validation_size: (float, optional), Defaults to 0.15
        Size of validation set as a ratio
    n_estimators: (int, optional), Defaults to 256
        Number of trees in the random forest
    min_df: (int, optional), Defaults to 5
        Removes all words from TF-IDF vectors that occur less than `min_df` times in the corpus
    max_df: (float, optional), Defaults to 0.8
        Removes all words from TF-IDF vectors that occur with frequency > 80% in the corpus
    ----------

    Returns
    ----------
    results: [dict]
        Test set along with labels
    Accuracy: float
        Accuracy on validation set, None if validation is False
    f1_score: float
       Macro F1 Score on validation set, None if validation is False
    ----------
    """
    tf_idf_vectorizer = TfidfVectorizer(min_df=min_df, max_df=max_df)

    documents = [row['tweet'] for row in train_data]
    labels = [row['label'] for row in train_data]
    vectors = tf_idf_vectorizer.fit_transform(documents)

    if validation:
        vectors_train, vectors_validation, labels_train, labels_validation = train_test_split(
            vectors, labels, test_size=validation_size)
    else:
        vectors_train, labels_train = vectors, labels

    classifier = RandomForestClassifier(n_estimators=n_estimators)
    classifier.fit(vectors_train, labels_train)
    accuracy = None
    f1_macro = None

    if validation:
        y_pred = classifier.predict(vectors_validation)
        accuracy = metrics.accuracy_score(labels_validation, y_pred)
        f1_macro = metrics.f1_score(
            labels_validation, y_pred, average="macro")

        classifier.fit(vectors, labels)

    test_documents = [row['tweet'] for row in test_data]
    test_vectors = tf_idf_vectorizer.transform(test_documents)
    y_pred = classifier.predict(test_vectors)

    results = []
    for i, tweet in enumerate(test_data):
        t = {
            'id': tweet['id'],
            'tweet': tweet['tweet'],
            'label': y_pred[i]
        }
        results.append(t)

    return results, accuracy, f1_macro
