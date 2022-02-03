import requests

def get_text(num_sentences=3):
	metaphorpsum_url = f'http://metaphorpsum.com/sentences/{num_sentences}'
	
	try:
		response = requests.get(metaphorpsum_url, timeout=5)
	except:
		pass
		
	return(response.text)

