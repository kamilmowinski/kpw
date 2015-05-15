from django.http import HttpResponseRedirect
from pydoc import locate

from django.views.generic import TemplateView, View
from django.conf import settings
from nltk.corpus import wordnet as wn

from .models import Statistic


class HomePage(TemplateView):
    template_name = 'kpw/index.html'


class SearchView(TemplateView):
    template_name = 'kpw/index.html'
    search_engine = locate(settings.SEARCH_CLASS)

    def get_context_data(self, **kwargs):
        ctx = super(SearchView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q', None)
        print q

        if q:
            queries = self.get_another_query(q)
            results = self.search_engine().query(queries)
            ctx['query_object'] = self.sort_query(results)
            ctx['query'] = q
        return ctx

    def get_another_query(self, q):
        ret = list()
        for query in q.split(' '):
            synsets = wn.synsets(query, pos=wn.NOUN)
            for synset in synsets:
                print synset.name(), synset.definition()
                ret.append(synset.name())
        ret += q.split(' ')
        return ret

    def sort_query(self, results):
        #urls = map(lambda x: x.uri, results)
        #stats = Statistic.objects.filter(
        #    url__in=urls, user=self.request.user)
        return results


class RedirectView(View):
    def post(self, request, *args, **kwargs):
        url = request.POST.get('uri', None)
        query = request.POST.get('query', None)
        if url:
            if request.user.is_authenticated():
                stat = Statistic.objects.get_or_create(
                    url=url, searched=query, user=request.user)[0]
                stat.count += 1
                stat.save()
            return HttpResponseRedirect(url)