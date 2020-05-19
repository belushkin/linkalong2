from utils import splitter


def test_read_stream():
    """
    Testing splitting functionality
    """

    # given
    text = "Hello. I am grut. No no no. Covid-19"

    # when
    # then
    assert ["Hello.", "I am grut.", "No no no.", "Covid-19"] == splitter.split(text)
