import requests
def search_movies(name):
	liste = []
	title = ('s={0}'.format(name))
	resp = requests.post('http://www.omdbapi.com/?i=tt3896198&apikey=27f3a92e&{}'.format(title))

	x = (resp.json())

	for counter in range(1,200):
		try:
			liste.append((x['Search'][counter]['Title']))
		except:
			return liste

def get_movie_info(title):
	resp = requests.post('http://www.omdbapi.com/?i=tt3896198&apikey=27f3a92e&t={}'.format(title))
	if resp.status_code != 200:
		raise ApiError('GET /tasks/ {}'.format(resp.status_code))
		return {"error": "external Api Down"}
	return resp