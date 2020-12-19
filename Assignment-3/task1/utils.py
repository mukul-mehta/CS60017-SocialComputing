import string
from configparser import ConfigParser


def read_config(filename="config.ini", section=""):
    if not section:
        raise Exception("Section not specified")

    parser = ConfigParser()
    parser.optionxform = str
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            if param[1].lower() == "false":
                config[param[0]] = False
            elif param[1].lower() == "true":
                config[param[0]] = True
            else:
                config[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )
    return config


def preprocessTweets(raw_train_data, raw_test_data):
    """
    Preprocess tweets by removing punctuation and converting to lowercase
    """

    table = str.maketrans('', '', string.punctuation)
    train_data = []
    test_data = []

    for row in raw_train_data:
        tweet = row[1].split()
        cleanTweet = ' '.join([w.translate(table).lower() for w in tweet])
        t = {
            'id': row[0],
            'tweet': cleanTweet,
            'label': row[2]
        }
        train_data.append(t)

    for row in raw_test_data:
        tweet = row[1].split()
        cleanTweet = ' '.join([w.translate(table).lower() for w in tweet])
        t = {
            'id': row[0],
            'tweet': cleanTweet,
        }
        test_data.append(t)

    return train_data, test_data
