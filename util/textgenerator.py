import requests

metaphorpsum_url = 'http://metaphorpsum.com/sentences/'

def get_text(sentences=4):
	global metaphorpsum_url
	
	metaphorpsum_url += str(sentences)
	response = requests.get(metaphorpsum_url, timeout=5)
	
	return(response.text)

