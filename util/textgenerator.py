import requests


def get_text(num_sentences=3):
    metaphorpsum_url = f'http://metaphorpsum.com/sentences/{num_sentences}'

    try:
        response = requests.get(metaphorpsum_url, timeout=5)
    except requests.exceptions.ConnectionError:
        response = 'The quick brown fox jumps over the lazy dog'
        return response

    return(response.text)
