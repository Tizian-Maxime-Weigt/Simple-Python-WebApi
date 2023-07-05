from googleapiclient.discovery import build

API_KEY = 'AIzaSyAd2QzPiLueo1n7UF910rQpXc3e-QmT-ZI'
CX = '300f61ad1f18d4ea8'

my_api_key = API_KEY
my_cse_id = CX

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

results = google_search(
    'stackoverflow site:en.wikipedia.org', my_api_key, my_cse_id, num=10)

for result in results:
    print(result)