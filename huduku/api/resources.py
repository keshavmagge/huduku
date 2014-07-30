from django.conf import settings
from tastypie import fields
from tastypie.resources import Resource
from tastypie.paginator import Paginator

from solr import SolrConnection

from huduku.api.utils import solr_escape, query_join
from huduku.api.paginator import SolrPaginator

solr = SolrConnection(settings.SOLR)

class SolrObject(object):
    def __init__(self, initial_data=None, **kwargs):
        self.__dict__['_data'] = initial_data or {}
    def __getattr__(self, key):
        return self._data.get(key, None)
    def to_dict(self):
        return self._data

class SolrResource(Resource):
    id = fields.CharField(attribute='id', default='id')
    name = fields.CharField(attribute='name', default='name')
    brand = fields.CharField(attribute='brand', default='brand')
    merchant = fields.CharField(attribute='merchant', default='merchant')
    category = fields.CharField(attribute='category', null=True, blank=True)
    age = fields.CharField(attribute='age', null=True, blank=True)
    gender = fields.CharField(attribute='gender', null=True, blank=True)
    price = fields.DecimalField(attribute='price', null=True, blank=True)
    sale_price = fields.DecimalField(attribute='sale_price', null=True, blank=True)
    buy_url = fields.CharField(attribute='buy_url', default='')
    image = fields.CharField(attribute='image', default='')

    class Meta:
        fields = ('name', 'brand', 'merchant', 'category', 'age', 'gender', 
                  'price', 'sale_price', 'buy_url', 'image',)
        resource_name = 'search'
        object_class = SolrObject
        collection_name = 'products'
        paginator_class = SolrPaginator

    def _get_solr_query(self, request):
        """
        takes as input request and returns a query
        that can be run on solr
        """
        query = []
        d = request.GET
        for param in d:
            if param in self._meta.fields:
                query.append(query_join(solr_escape(d[param]).split(' '), param)) 
        if not query:
            return '*:*'
        return ' '.join(query)

    def _get_faceting_params(self):
        return {'facet': 'true','facet_field': ['gender', 'str_category', 
                                                'str_brand', 'str_merchant'],
                'facet_range': 'price', 'f_price_facet_range_start': 0, 
                'f_price_facet_range_end': 1000, 'f_price_facet_range_gap': 50,
                'facet_mincount': 1}

    def dehydrate_facets(self, solr_response):
        """
        takes SolrResponse object as input and returns facets information
        for use in an API response
        """
        facets = {}
        for facet_range in solr_response.facet_counts.get('facet_ranges').keys(): 
            facets[facet_range] = solr_response.facet_counts.get('facet_ranges'
                                       )[facet_range]['counts']
        for facet_field in solr_response.facet_counts.get('facet_fields').keys():
            # do not overwrite if facet field is a range facet too
            facet_field_label = facet_field.lstrip('str_')
            facets[facet_field_label] = facets.get(facet_field, None) or \
                                  solr_response.facet_counts.get('facet_fields'
                                       )[facet_field]
        return facets

    def dehydrate_price(self, bundle):
        """
        set precision to 2 decimal digits
        """
        return ("%.2f" % round(bundle.obj.price,2))

    def dehydrate_sale_price(self, bundle):
        """
        set precision to 2 decimal digits
        """
        if bundle.obj.sale_price:
            return ("%.2f" % round(bundle.obj.sale_price,2))
        return None

    def _get_pagination_params(self, request):
        """
        given a request object, returns the start and rows that is used in
        the solr query
        """
        start = request.GET.get('offset', 0)
        rows = request.GET.get('limit', 20)
        return {'start': start, 'rows': rows}

    def get_object_list(self, request, **kwargs):
        query = self._get_solr_query(request)
        params = self._get_faceting_params()
        params.update(self._get_pagination_params(request))
        response = solr.query(query, **params)
       
        results = [SolrObject(initial_data=res) for res in response.results]
        facets = self.dehydrate_facets(response)
        return results, facets, response.numFound

    def obj_get_list(self, bundle, **kwargs):
        query = bundle.request.GET.get('query', None)
        if query:
            self._meta.query = query
        return self.get_object_list(bundle.request, query=query)
    
    def get_list(self, request, **kwargs):
        base_bundle = self.build_bundle(request=request)
        objects, facets, count = self.obj_get_list(bundle=base_bundle, 
                                   **self.remove_api_resource_names(kwargs))
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(request.GET, sorted_objects, 
                       resource_uri=self.get_resource_uri(), limit=self._meta.limit, 
                       max_limit=self._meta.max_limit, collection_name=self._meta.collection_name,
                       object_count=count)
        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        bundles = []

        for obj in to_be_serialized[self._meta.collection_name]:
            bundle = self.build_bundle(obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle, for_list=True))

        to_be_serialized[self._meta.collection_name] = bundles
        to_be_serialized['facets'] = facets
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        return self.create_response(request, to_be_serialized)

    def obj_get(self, request=None, **kwargs):
        return self.get_object_list(request, query='id:%s' % kwargs['pk'])[0]
