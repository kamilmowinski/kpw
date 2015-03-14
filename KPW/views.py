__author__ = 'Kamil Mówiński'
from django.views.generic import TemplateView
from nltk.corpus import wordnet as wn


class HomePage(TemplateView):
    template_name = 'kpw/index.html'


class SearchView(TemplateView):
    template_name = 'kpw/index.html'

    def get_context_data(self, **kwargs):
        ctx = super(SearchView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q', None)
        if q:
            ctx['query_list'] = self.get_another_query(q)
        return ctx

    def get_another_query(self, q):
        synsets = wn.synsets(q, pos=wn.NOUN)
        ret = list()
        for synset in synsets:
            ret.append((synset.lexname(), synset.definition()))
        return ret