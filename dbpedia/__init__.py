from string import Template
from SPARQLWrapper import SPARQLWrapper, JSON
from KPW.classes import SearchResult


class DBpediaSearch:
    URL = "http://dbpedia.org/sparql"

    def __init__(self):
        pass

    def keywords(self, queries):
        lower_queries = map(unicode.lower, queries)
        if 'sameas' in lower_queries:
            return '<http://www.w3.org/2002/07/owl#sameAs>'
        if 'abstract' in lower_queries:
            return '<http://dbpedia.org/ontology/abstract>'
        if 'subject' in lower_queries:
            return '<http://purl.org/dc/terms/subject>'
        if 'label' in lower_queries:
            return '<http://www.w3.org/2000/01/rdf-schema#label>'
        if 'type' in lower_queries:
            return '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'
        if 'external' in lower_queries:
            return '<http://dbpedia.org/ontology/wikiPageExternalLink>'
        return None

    def query(self, queries):
        ret = dict()
        queries = set(map(lambda x: x.split('.')[0], queries))
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        key = self.keywords(queries)
        for query in queries:
            if key:
                sparquery = Template("""
                SELECT ?o
                WHERE { <http://dbpedia.org/resource/$query> $key ?o }
                """)
                sparquery = sparquery.substitute(query=query.title(), key=key)
            else:
                sparquery = Template("""
                SELECT ?c ?o
                WHERE { <http://dbpedia.org/resource/$query> ?c ?o }
                """)
                sparquery = sparquery.substitute(query=query.title())
            sparql.setQuery(sparquery)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            for result in results['results']['bindings']:
                if result['o']['value'] in ret:
                    ret[result['o']['value']].key_words.append(query)
                else:
                    ret[result['o']['value']] = SearchResult(result['o']['value'], result['o']['value'],
                                                             "", [query, ])
        return ret.values()

