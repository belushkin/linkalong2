import nltk

nltk.download('punkt')


def split(text):
    """
    Function for splitting text into sentences

    >>> split("Hello. I am grut. No no no. Covid-19")
    ["Hello", "I am grut", "No no no", "Covid-19"]
    >>> split("Hello")
    ["Hello"]
    >>> split("")
    []

    :param text: String up to 1 mb
    :return: List of strings
    """
    sentences = nltk.tokenize.sent_tokenize(text)

    return sentences
