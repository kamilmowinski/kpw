import requests

from KPW.classes import SearchResult


class GoogleSearch:
    URI = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q={}"

    def __init__(self):
        pass

    def query(self, queries):
        ret = dict()
        for query in queries:
            r = requests.get(self.URI.format(query.split('.')[0]))
            json_data = r.json()
            if json_data['responseStatus'] == 200:
                for page in json_data['responseData']['results']:
                    if page['url'] in ret:
                        ret[page['url']].key_words.append(query)
                    else:
                        ret[page['url']] = SearchResult(page['url'], page['titleNoFormatting'],
                                                        page['content'], [query, ])
            else:
                raise ValueError(json_data['responseDetails'])
        return ret.values()

