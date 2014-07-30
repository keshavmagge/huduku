from django.conf.urls import patterns, url, include
from django.conf import settings

from huduku.api.resources import SolrResource

solr_resource = SolrResource()

urlpatterns = patterns('',
    (r'^api/', include(solr_resource.urls)),
)
