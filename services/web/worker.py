from flask import jsonify


def process_worker(url):

    print(url)
    return jsonify(hello="mesama")
