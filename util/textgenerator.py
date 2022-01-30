import requests

def get_text(num_sentences=3):
	metaphorpsum_url = f'http://metaphorpsum.com/sentences/{num_sentences}'

	response = requests.get(metaphorpsum_url, timeout=5)
	
	return(response.text)

