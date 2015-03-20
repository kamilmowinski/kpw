from django.http import HttpResponseRedirect

__author__ = 'Kamil Mówiński'
from pydoc import locate

from django.views.generic import TemplateView, View
from django.conf import settings
from nltk.corpus import wordnet as wn


class HomePage(TemplateView):
    template_name = 'kpw/index.html'


class SearchView(TemplateView):
    template_name = 'kpw/index.html'
    search_engine = locate(settings.SEARCH_CLASS)

    def get_context_data(self, **kwargs):
        ctx = super(SearchView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q', None)
        if q:
            queries = self.get_another_query(q)
            result = self.search_engine().query(queries)
            ctx['query_object'] = sorted(result,
                                         key=lambda x: x.probability)
        return ctx

    def get_another_query(self, q):
        synsets = wn.synsets(q, pos=wn.NOUN)
        ret = list()
        for synset in synsets:
            ret.append(synset.name())
        return ret


class RedirectView(View):
    def get(self, request, *args, **kwargs):
        url = kwargs.get('url', None)
        if url:
            return HttpResponseRedirect(url)